from __future__ import print_function # In python 2.7
import sys

# -*- coding: utf-8 -*-

###########################################################
# Retrieve robot audio buffer
# Syntaxe:
#    python scriptname --pip <ip> --pport <port>
#
#    --pip <ip>: specify the ip of your robot (without specification it will use the NAO_IP defined some line below
#
# Author: Alexandre Mazel
###########################################################


import naoqi
import sounddevice as sd
import numpy as np
import StringIO
import time
import sys
import Queue as q
import scipy.io.wavfile as sp
import pyaudio
import wave

class SoundReceiverModule(naoqi.ALModule):
    """
    Use this object to get call back from the ALMemory of the naoqi world.
    Your callback needs to be a method with two parameter (variable name, value).
    """

    def __init__( self, strModuleName, strNaoIp, strNaoPort ):
        try:
            naoqi.ALModule.__init__(self, strModuleName);
            self.BIND_PYTHON(self.getName(), "callback");
            self.strNaoIp = strNaoIp
            self.pport = strNaoPort
            self.outfile = None
            self.aOutfile = [None]*(4-1) # ASSUME max nbr channels = 4
            self.nSampleRate = 48000 # or sampling rate could be 16000
            self.channelQ = q.Queue()
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
        print( "INF: SoundReceiver: stopped!" )
        if( self.outfile != None ):
            self.outfile.close();

    def processRemote( self, nbOfChannels, nbrOfSamplesByChannel, aTimeStamp, buffer):
        """
        This is THE method that receives all the sound buffers from the "ALAudioDevice" module
        """
        print( "process!" , file=sys.stderr)
        # print( "processRemote: %s, %s, %s, lendata: %s, data0: %s (0x%x), data1: %s (0x%x)" % (nbOfChannels, nbrOfSamplesByChannel, aTimeStamp, len(buffer), buffer[0],ord(buffer[0]),buffer[1],ord(buffer[1])) );
        # print( "raw data: " ),
        # for i in range( 8 ):
        #     print( "%s (0x%x), " % (buffer[i],ord(buffer[i])) , file=sys.stderr),
        # print( "" , file=sys.stderr)

        aSoundDataInterlaced = np.fromstring( str(buffer), dtype=np.int16 );
        # print( "len data: %s " % len( aSoundDataInterlaced ) );
        # print( "data interlaced: " ),
        # for i in range( 8 ):
        #     print( "%d, " % (aSoundDataInterlaced[i]) ),
        # print( "" );
        aSoundData = np.reshape( aSoundDataInterlaced, (nbOfChannels, nbrOfSamplesByChannel), 'F' );
        # numrows = len(aSoundData)
        # numcols = len(aSoundData[0])
        # print("Rows:", numrows, "\tCols:", numcols)
        inputdata = aSoundData[0,:]
        self.channelQ.put(inputdata) # Add data from this channel to the queue
        # print(self.channelQ.qsize())
        # threading.Thread(target=sd.play(aSoundData[0], 48000, blocking=False))
        # print( "len data: %s " % len( self.aSoundData ) );
        # print( "len data 0: %s " % len( self.aSoundData[0] ) );
        if( False ):
            # compute average
            aAvgValue = np.mean( aSoundData, axis = 1 );
            print( "avg: %s" % aAvgValue );
        if( False ):
            # compute fft
            nBlockSize = nbrOfSamplesByChannel;
            signal = aSoundData[0] * np.hanning( nBlockSize );
            aFft = ( np.fft.rfft(signal) / nBlockSize );
            print ("%s",aFft);
        if( False ):
            # compute peak
            aPeakValue = np.max( aSoundData );
            if( aPeakValue > 16000 ):
                print( "Peak: %s" % aPeakValue );
        if( False ):
            bSaveAll = False; #True
            # save to file
            if( self.outfile == None ):
                strFilenameOut = "../nao_robot_video_streaming/test.wav"; # CHANGE THIS
                print( "INF: Writing sound to '%s'" % strFilenameOut );
                self.outfile = open( strFilenameOut, "wb" );
                if( bSaveAll ):
                    for nNumChannel in range( 1, nbOfChannels ):
                        strFilenameOutChan = strFilenameOut.replace(".wav", "_%d.wav"%nNumChannel);
                        self.aOutfile[nNumChannel-1] = open( strFilenameOutChan, "wb" );
                        print( "INF: Writing other channel sound to '%s'" % strFilenameOutChan );

            # sf.write(strFilenameOut, aSoundDataInterlaced, self.nSampleRate, subtype=None, endian=None, format='WAV', closefd=True)
            # aSoundDataInterlaced.tofile( self.outfile ); # wrote the 4 channels
            # aSoundData[0].tofile( self.outfile ); # wrote only one channel
            # print( "aTimeStamp: %s" % aTimeStamp );
            # print( "data written: " ),
            # for i in range( 8 ):
            #     print( "%d, " % (self.aSoundData[0][i]) ),
            # print( "" );
            #self.stop(); # make naoqi crashes
            if( bSaveAll ):
                for nNumChannel in range( 1, nbOfChannels ):
                    self.aSoundData[nNumChannel].tofile( self.aOutfile[nNumChannel-1] );
    # processRemote - end

    def get_audio(self):
        # print("Playing:", file=sys.stderr)
        if(self.channelQ.empty() == False):
            # print(self.channelQ.qsize())
            buf = StringIO.StringIO()
            channel_1 = self.channelQ.get() #Dequeue from our data from channel 0

            # Write our channel data into a .WAV file format
            # Use the StringIO buf to mimic a file stream
            sp.write(buf, 48000, channel_1) #Input data from the channel is a 16-bit integer

            wav = buf.getvalue()
            print("Playing:", file=sys.stderr)
            chunk = 1024
            wf = wave.open(buf, 'rb')
            p = pyaudio.PyAudio()

            stream = p.open(
                format=p.get_format_from_width(wf.getsampwidth()),
                channels=wf.getnchannels(),
                rate=wf.getframerate(),
                output=True)
            data = wf.readframes(chunk)

            while data != '':
                stream.write(data)
                data = wf.readframes(chunk)

            stream.close()
            p.terminate()

            return wav
            # print(channel_1, file=sys.stderr);
            # size = len(channel_1)
            # for i in range(0, size):
            #     print(channel_1[i], file=sys.stderr)
            # dataSize = len(channel_1)
            # print(dataSize, file=sys.stderr)
            #sd.play(channel_1, 48000, blocking=True)


    def version( self ):
        return "0.6";

# SoundReceiver - end