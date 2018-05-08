from __future__ import print_function # In python 2.7

# -*- coding: utf-8 -*-

###########################################################
# Retrieve robot audio buffer
# Sample Rate: 48000
# Number of Samples: 4096
# Gets one channel of audio (configurable up to 4)
# Datatype int16
###########################################################


import naoqi
import sounddevice as sd
import numpy as np
import sys
import Queue as q
import pyaudio
import threading
from collections import deque
from scipy.signal import butter, lfilter


class SoundReceiverModule(naoqi.ALModule):
    """
    Use this object to get call back from the ALMemory of the naoqi world.
    Your callback needs to be a method with two parameter (variable name, value).
    """

    def __init__(self, strModuleName, strNaoIp, pport):
        try:
            naoqi.ALModule.__init__(self, strModuleName)
        except BaseException, err:
            print("ERR: abcdk.naoqitools.SoundReceiverModule: loading error: %s" % str(err))
        self.BIND_PYTHON(self.getName(), "callback")
        self.strNaoIp = strNaoIp
        self.pport = pport
        self.outfile = None
        self.aOutfile = [None]*(4-1)  # ASSUME max nbr channels = 4
        self.nSampleRate = 48000  # or sampling rate could be 16000
        self.audioDeque = deque([])
        self.audioDeque_receive = deque([])
        self.thread1 = None

    def __del__(self):
        print("INF: abcdk.SoundReceiverModule.__del__: cleaning everything")
        self.stop()

    def start(self):
        audioProxy = naoqi.ALProxy("ALAudioDevice", self.strNaoIp, self.pport) # establish proxy to nao
        nNbrChannelFlag = 0  # ALL_Channels: 0,  AL::LEFTCHANNEL: 1, AL::RIGHTCHANNEL: 2; AL::FRONTCHANNEL: 3  or AL::REARCHANNEL: 4.
        nDeinterleave = 0
        audioProxy.setClientPreferences(self.getName(), self.nSampleRate, nNbrChannelFlag, nDeinterleave)
        audioProxy.subscribe(self.getName())  # subscribe to naos microphones
        print("INF: SoundReceiver: started!")

    def stop(self):
        print("INF: SoundReceiver: stopping...")
        audioProxy = naoqi.ALProxy("ALAudioDevice", self.strNaoIp, self.pport)
        audioProxy.unsubscribe(self.getName())  # unsubscribe from naos microphones
        self.thread1.join()  # wait for thread1 (playing of audio) to finish
        print("INF: SoundReceiver: stopped!")

    def processRemote(self, nbOfChannels, nbrOfSamplesByChannel, aTimeStamp, buffer):
        """
        This is THE method that receives all the sound buffers from the "ALAudioDevice" module
        """
        aSoundDataInterlaced = np.fromstring(str(buffer), dtype=np.int16)
        aSoundData = np.reshape(aSoundDataInterlaced, (nbOfChannels, nbrOfSamplesByChannel), 'F')

        # filter audio data
        # ****************** bandpass
        lowcut = 300 # don't go below 150, sweet spot is 300
        highcut = 3000 # don't do 1000
        y = self.butter_bandpass_filter(aSoundData[0, :], lowcut, highcut, self.nSampleRate, order=6)

        self.audioDeque.append(y)

    # Create filter functions
    def butter_lowpass(self, cutoff, fs, order):
        nyq = 0.5 * fs
        normal_cutoff = cutoff / nyq
        b, a = butter(order, normal_cutoff, btype='low')
        return b, a

    def butter_lowpass_filter(self, data, cutoff, fs, order):
        b, a = self.butter_lowpass(cutoff, fs, order=order)
        y = lfilter(b, a, data)
        return y

    def butter_bandpass(self, lowcut, highcut, fs, order):
        nyq = 0.5 * fs
        low = lowcut / nyq
        high = highcut / nyq

        b, a = butter(order, [low, high], btype='band')
        return b, a

    def butter_bandpass_filter(self, data, lowcut, highcut, fs, order):
        b, a = self.butter_bandpass(lowcut, highcut, fs, order=order)
        y = lfilter(b, a, data)
        return y

    def play_audio(self, stop):
        # plays audio from deque until stop flag is set
        while True:
            while((len(self.audioDeque_receive) != 0) and (not stop.is_set())):
                samples = self.audioDeque_receive.popleft()
                sd.play(samples, self.nSampleRate, blocking= False)
            if stop.is_set():
                print('stop play 2')
                break

    def get_audio(self, stop):
        print("Playing:", file=sys.stderr)
        # sets up a thread to play the audio while the main thread processes incoming audio
        self.thread1 = threading.Thread(target=self.play_audio, args=(stop,))
        self.thread1.daemon = True
        self.thread1.start()

        while(not stop.is_set()):
            if(len(self.audioDeque) > 15):
                # generate samples, note conversion to float32 array
                samples1 = self.audioDeque.popleft().astype(np.float32, order='C') / 32768.0
                samples2 = self.audioDeque.popleft().astype(np.float32, order='C') / 32768.0
                samples3 = self.audioDeque.popleft().astype(np.float32, order='C') / 32768.0
                samples4 = self.audioDeque.popleft().astype(np.float32, order='C') / 32768.0
                samples5 = self.audioDeque.popleft().astype(np.float32, order='C') / 32768.0
                samples6 = self.audioDeque.popleft().astype(np.float32, order='C') / 32768.0
                samples7 = self.audioDeque.popleft().astype(np.float32, order='C') / 32768.0
                samples8 = self.audioDeque.popleft().astype(np.float32, order='C') / 32768.0
                samples9 = self.audioDeque.popleft().astype(np.float32, order='C') / 32768.0
                samples10 = self.audioDeque.popleft().astype(np.float32, order='C') / 32768.0
                samples11 = self.audioDeque.popleft().astype(np.float32, order='C') / 32768.0
                samples12 = self.audioDeque.popleft().astype(np.float32, order='C') / 32768.0
                samples13 = self.audioDeque.popleft().astype(np.float32, order='C') / 32768.0
                samples14 = self.audioDeque.popleft().astype(np.float32, order='C') / 32768.0
                samples15 = self.audioDeque.popleft().astype(np.float32, order='C') / 32768.0
                samples = np.concatenate((samples1, samples2, samples3, samples4, samples5, samples6, samples7, samples8, samples9, samples10, samples11, samples12, samples13, samples14, samples15))
                # puts all of the samples into the deque to be played by other thread
                self.audioDeque_receive.append(samples)
        print('stop play 1')
        self.__del__()
        return

    def version(self):
        return "0.6"
