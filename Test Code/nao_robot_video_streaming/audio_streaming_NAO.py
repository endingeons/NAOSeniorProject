from __future__ import print_function # In python 2.7
import sys

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

    def __init__( self, strModuleName, strNaoIp, pport):
        try:
            naoqi.ALModule.__init__(self, strModuleName);
            self.BIND_PYTHON(self.getName(), "callback");
            self.strNaoIp = strNaoIp
            self.pport = pport;
            self.outfile = None
            self.aOutfile = [None]*(4-1) # ASSUME max nbr channels = 4
            self.nSampleRate = 48000 # or sampling rate could be 16000
            # self.channelQ = q.Queue()
            self.audioDeque = deque([])
            self.audioDeque_receive = deque([])
            # self.p = pyaudio.PyAudio()
            self.thread1 = None # = threading.Thread(target= self.play_audio, args=[])
            # # self.thread2 = threading.Thread(target= self.play_audio, args=[])
            # # Setting up stream for audio output
            # # fs = self.nSampleRate  # sampling rate, Hz, must be integer
            # # for paFloat32 sample values must be in range [-1.0, 1.0]
            # # self.stream = self.p.open(format=pyaudio.paFloat32,
            # #                      channels=1,
            # #                      rate=fs,
            # #                      output=True)

        except BaseException, err:
            print( "ERR: abcdk.naoqitools.SoundReceiverModule: loading error: %s" % str(err) );

    # __init__ - end
    def __del__( self ):
        print( "INF: abcdk.SoundReceiverModule.__del__: cleaning everything" );
        self.stop()

    def start( self ):
        audioProxy = naoqi.ALProxy("ALAudioDevice", self.strNaoIp, self.pport);
        nNbrChannelFlag = 0;  # ALL_Channels: 0,  AL::LEFTCHANNEL: 1, AL::RIGHTCHANNEL: 2; AL::FRONTCHANNEL: 3  or AL::REARCHANNEL: 4.
        nDeinterleave = 0;
        audioProxy.setClientPreferences(self.getName(), self.nSampleRate, nNbrChannelFlag,
                                             nDeinterleave);  # setting same as default generate a bug !?!
        audioProxy.subscribe(self.getName());
        print("INF: SoundReceiver: started!");
        # self.processRemote( 4, 128, [18,0], "A"*128*4*2 ) # for local test

        # on romeo, here's the current order:
        # 0: right;  1: rear;   2: left;   3: front,

    def stop( self ):
        print( "INF: SoundReceiver: stopping..." )
        audioProxy = naoqi.ALProxy( "ALAudioDevice", self.strNaoIp, self.pport );
        audioProxy.unsubscribe( self.getName() );
        self.thread1.join()
        self.thread2.join()
        print( "INF: SoundReceiver: stopped!" )
        # if( self.outfile != None ):
        #     self.outfile.close();
        self.stream.close()

    def processRemote( self, nbOfChannels, nbrOfSamplesByChannel, aTimeStamp, buffer):
        """
        This is THE method that receives all the sound buffers from the "ALAudioDevice" module
        """
        # print( "process!" , file=sys.stderr)
        # print( "processRemote: nbOfChannels %s, \nnbrOFSamplesByChannel%s, \naTimeStamp%s, \nlendata: %s, data0: %s (0x%x), data1: %s (0x%x)" % (nbOfChannels, nbrOfSamplesByChannel, aTimeStamp, len(buffer), buffer[0],ord(buffer[0]),buffer[1],ord(buffer[1])) );
        # print( "raw data: " ),
        # for i in range( 1000 ):
        #     print( "%s (0x%x), " % (buffer[i],ord(buffer[i])) , file=sys.stderr),
        # print( "" , file=sys.stderr)

        aSoundDataInterlaced = np.fromstring( str(buffer), dtype=np.int16);
        # print( "len data: %s " % len( aSoundDataInterlaced ) );
        # print( "data interlaced: " ),
        # for i in range( 8 ):
        #     print( "%d, " % (aSoundDataInterlaced[i]) ),
        # print( "" );
        aSoundData = np.reshape( aSoundDataInterlaced, (nbOfChannels, nbrOfSamplesByChannel), 'F' );
        # numrows = len(aSoundData)
        # numcols = len(aSoundData[0])
        # print("Rows:", numrows, "\tCols:", numcols)

        # filter audio data
        # ****************** bandpass
        lowcut = 400 #don't go below 150, sweet spot is 300
        highcut = 3000 #don't do 1000
        y = self.butter_bandpass_filter(aSoundData[0,:], lowcut, highcut, self.nSampleRate, order=6)
        inputdata = y

        # ***************** lowpass
        # cutoff = 1000
        # y = self.butter_lowpass_filter(self, aSoundData[0,:], cutoff, self.nSampleRate, order=5)
        # inputdata = y

        # inputdata = aSoundData[0,:]
        self.audioDeque.append(inputdata)
        # self.channelQ.put(inputdata) # Add data from this channel to the queue

    # processRemote - end

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
        volume = 0.9
        while True:
            while((len(self.audioDeque_receive) != 0) and (not stop.is_set())):
                samples = self.audioDeque_receive.popleft()
                sd.play(samples, self.nSampleRate, blocking= False)
                # self.stream.write(volume * samples)
            if stop.is_set():
                print('stop play 2')
                break
    # play_audio - end

    def get_audio(self, stop):
        print("Playing:", file=sys.stderr)
        self.thread1 = threading.Thread(target=self.play_audio, args=(stop,))
        self.thread1.daemon = True
        self.thread1.start()

        #self.thread2.start()
        # time.sleep(5)
        while(not stop.is_set()):
            if(len(self.audioDeque) > 11):
                # print(self.channelQ.qsize())
                # print("", file=sys.stderr)
                volume = 0.9  # range [0.0, 1.0]

                # generate samples, note conversion to float32 array
                # samples1 = self.channelQ.get().astype(np.float32, order='C') / 32768.0
                # samples2 = self.channelQ.get().astype(np.float32, order='C') / 32768.0
                # samples3 = self.channelQ.get().astype(np.float32, order='C') / 32768.0
                # samples4 = self.channelQ.get().astype(np.float32, order='C') / 32768.0
                # samples5 = self.channelQ.get().astype(np.float32, order='C') / 32768.0
                # samples6 = self.channelQ.get().astype(np.float32, order='C') / 32768.0
                # samples7 = self.channelQ.get().astype(np.float32, order='C') / 32768.0
                # samples8 = self.channelQ.get().astype(np.float32, order='C') / 32768.0

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
                samples = np.concatenate((samples1, samples2, samples3, samples4, samples5, samples6, samples7, samples8, samples9, samples10, samples11))
                # play. May repeat with different volume values (if done interactively)
                self.audioDeque_receive.append(samples)
                # sd.play(samples, self.nSampleRate)
                # sd.wait()
                # sd.stop()
                # self.stream.write(volume * samples)
                # self.stream.stop_stream()
                # self.stream.close()
                # self.p.terminate()
            # else:
            #     continue
        # # Poll for queue size
        # while(self.channelQ.qsize() < 8):
        #     continue
        #
        # samples1 = self.channelQ.get().astype(np.int16, order='C')
        # samples2 = self.channelQ.get().astype(np.int16, order='C')
        # samples3 = self.channelQ.get().astype(np.int16, order='C')
        # samples4 = self.channelQ.get().astype(np.int16, order='C')
        # samples5 = self.channelQ.get().astype(np.int16, order='C')
        # samples6 = self.channelQ.get().astype(np.int16, order='C')
        # samples7 = self.channelQ.get().astype(np.int16, order='C')
        # samples8 = self.channelQ.get().astype(np.int16, order='C')
        # channel_1 = np.concatenate((samples1, samples2, samples3, samples4, samples5, samples6, samples7, samples8))
        # print(channel_1)
        # #https://stackoverflow.com/questions/33879523/python-how-can-i-generate-a-wav-file-with-beeps
        #
        # # Dequeue from our data from channel 0
        # # channel_1 = self.channelQ.get()
        #
        # # Use the StringIO buf to mimic a file stream
        # bytestream = io.BytesIO()
        # buf = StringIO.StringIO()
        # wav_file = wave.open(bytestream, "w")
        # nchannels = 1
        # sampwidth = 2
        # nframes = len(channel_1)
        # comptype = "NONE"
        # compname = "not compressed"
        # wav_file.setparams((nchannels, sampwidth, self.nSampleRate, nframes, comptype, compname))
        #
        # # Write our channel data into a .WAV file format
        # # Input data from the channel is a 16-bit integer
        # for sample in channel_1:
        #     wav_file.writeframes(struct.pack('h', int(sample)))
        # # wav = buf.getvalue()
        # wav_file.close()
        # return bytestream
        print('stop play 1')
        return

    def version( self ):
        return "0.6";

# SoundReceiver - end