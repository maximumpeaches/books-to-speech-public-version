from google.cloud import texttospeech

client = texttospeech.TextToSpeechClient()


def synthesize_text(text):
    # Set the text input to be synthesized
    synthesis_input = texttospeech.SynthesisInput(text=text)

    # Build the voice request, select the language code ("en-US") and the ssml
    # voice gender ("neutral")
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )

    # Select the type of audio file you want returned
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    # Perform the text-to-speech request on the text input with the selected
    # voice parameters and audio file type
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )
    return response.audio_content


bytes_in_each_space = len(' '.encode('utf-8'))


def split_text_into_chunks(chapter):
    words = chapter.split(' ')
    # Remove the empty space around each word, or else things could get weird when we add the spaces back in.
    words = [word.strip() for word in words]
    byte_count = 0
    # We should be able to send 5,000 bytes at once, but maybe there's a bug in my code or something because it keeps
    # saying I'm going over that limit, so I adjusted it lower than 5,000, which is fine.
    max_bytes_per_api_call = 1000
    sentences_for_synthesis = []
    i = 0
    chunks = []
    while i < len(words):
        sentence = words[i]
        num_bytes = len(sentence.encode('utf-8'))
        # If we reached the max request size for Google's text-to-speech service, then we want to save the audio content and reset the variable.
        # Add the 5 to the byte count just for good measure.
        if num_bytes + byte_count + bytes_in_each_space + 5 >= max_bytes_per_api_call:
            if sentences_for_synthesis is None:
                raise Exception(
                    'looks like a single sentence was too big. This shouldn\'t happen often if ever, so the code doesn\'t handle it well. Maybe you can check if there were periods in the initial sentence?')
            # i is not incremented because we need to add it in the next loop
            # Add the spaces back in. Paragraph spacing and new lines will have been removed.
            chunks.append(' '.join(sentences_for_synthesis))
            sentences_for_synthesis = []
            byte_count = 0
        else:
            i += 1
            sentences_for_synthesis.append(sentence)
            byte_count += num_bytes

    # Add anything leftover after the loop above completed.
    if sentences_for_synthesis is not None:
        chunks.append(' '.join(sentences_for_synthesis))

    return chunks


def convert_text_to_audio_snippets(text):
    chunks = split_text_into_chunks(text)
    return [synthesize_text(chunk) for chunk in chunks]
