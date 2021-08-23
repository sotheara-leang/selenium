import os
import time
import wave

import pyaudio
from selenium import webdriver
from selenium.webdriver.support.select import Select


def decode_using_google_api(spk_dir, output_dir):
    # init driver
    GOOGLE_ASR_API = 'https://www.google.com/intl/en/chrome/demos/speech.html'

    option = webdriver.ChromeOptions()
    # option.add_argument('headless')
    option.add_experimental_option('prefs', {
        "profile.default_content_setting_values.media_stream_mic": 1,
    })
    driver = webdriver.Chrome('./chromedriver', options=option)
    driver.get(GOOGLE_ASR_API)

    # select language
    select_language = Select(driver.find_element_by_id('select_language'))
    select_language.select_by_value('23')

    start_button = driver.find_element_by_id('start_button')

    for idx, wav_file in enumerate(os.scandir('%s/wav' % spk_dir)):
        if wav_file.is_dir() or wav_file.name.startswith('.') or wav_file.name.startswith('_'):
            continue

        # start mic button
        time.sleep(1)
        start_button.click()

        wav_filename = os.path.basename(wav_file.path)
        wav_filename, _ = os.path.splitext(wav_filename)

        print(f'playing wav file: {wav_file.path}')
        wf = wave.open(wav_file.path, 'rb')

        p_audio = pyaudio.PyAudio()
        stream = p_audio.open(format=p_audio.get_format_from_width(wf.getsampwidth()), channels=wf.getnchannels(),
                              rate=wf.getframerate(), output=True)

        while True:
            # read data in every 8000 bytes
            data = wf.readframes(8000)
            if len(data) == 0:
                break

            # play the sound by writing the audio data to the stream
            stream.write(data)

        # stop mic button
        start_button.click()

        print(f'stop playing wav file: {wav_file.path}')
        # close streams
        stream.close()
        p_audio.terminate()

        # get decoding trans
        div_results = driver.find_element_by_id('results')
        trans = div_results.text

        # write trans to file
        trans_file = open('%s/trans.csv' % output_dir, 'a', encoding='utf-8')
        trans_file.write('%s, %s\n' % (wav_filename, trans))
        trans_file.close()


if __name__ == '__main__':
    spk_dir = 'work/data/KM-01-F-30-40015'
    output_dir = 'work/result'

    decode_using_google_api(spk_dir, output_dir)
