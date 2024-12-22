from note_definer import NoteDefiner
from frequency_extractor import FrequencyExtractor


class MusicXmlCreator:
    file_head = \
"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE score-partwise PUBLIC "-//Recordare//DTD MusicXML 4.0 Partwise//EN" "http://www.musicxml.org/dtds/partwise.dtd">
<score-partwise version="4.0">
  <work>
    <work-title>Sound To Note</work-title>
    </work>
  <identification>
    <creator type="composer">STN</creator>
    <encoding>
      <software>MuseScore 4.4.3</software>
      <encoding-date>2024-11-24</encoding-date>
      <supports element="accidental" type="yes"/>
      <supports element="beam" type="yes"/>
      <supports element="print" attribute="new-page" type="yes" value="yes"/>
      <supports element="print" attribute="new-system" type="yes" value="yes"/>
      <supports element="stem" type="yes"/>
      </encoding>
    </identification>
  <defaults>
    <scaling>
      <millimeters>6.99911</millimeters>
      <tenths>40</tenths>
      </scaling>
    <page-layout>
      <page-height>1696.94</page-height>
      <page-width>1200.48</page-width>
      <page-margins type="even">
        <left-margin>85.7252</left-margin>
        <right-margin>85.7252</right-margin>
        <top-margin>85.7252</top-margin>
        <bottom-margin>85.7252</bottom-margin>
        </page-margins>
      <page-margins type="odd">
        <left-margin>85.7252</left-margin>
        <right-margin>85.7252</right-margin>
        <top-margin>85.7252</top-margin>
        <bottom-margin>85.7252</bottom-margin>
        </page-margins>
      </page-layout>
    <appearance>
      <line-width type="light barline">1.8</line-width>
      <line-width type="heavy barline">5.5</line-width>
      <line-width type="beam">5</line-width>
      <line-width type="bracket">4.5</line-width>
      <line-width type="dashes">1</line-width>
      <line-width type="enclosure">1</line-width>
      <line-width type="ending">1.1</line-width>
      <line-width type="extend">1</line-width>
      <line-width type="leger">1.6</line-width>
      <line-width type="pedal">1.1</line-width>
      <line-width type="octave shift">1.1</line-width>
      <line-width type="slur middle">2.1</line-width>
      <line-width type="slur tip">0.5</line-width>
      <line-width type="staff">1.1</line-width>
      <line-width type="stem">1</line-width>
      <line-width type="tie middle">2.1</line-width>
      <line-width type="tie tip">0.5</line-width>
      <line-width type="tuplet bracket">1</line-width>
      <line-width type="wedge">1.2</line-width>
      <note-size type="cue">70</note-size>
      <note-size type="grace">70</note-size>
      <note-size type="grace-cue">49</note-size>
      </appearance>
    <music-font font-family="Leland"/>
    <word-font font-family="Edwin" font-size="10"/>
    <lyric-font font-family="Edwin" font-size="10"/>
    </defaults>
  <credit page="1">
    <credit-type>title</credit-type>
    <credit-words default-x="600.241935" default-y="1611.210312" justify="center" valign="top" font-size="22">Sound To Note</credit-words>
    </credit>
  <credit page="1">
    <credit-type>subtitle</credit-type>
    <credit-words default-x="600.241935" default-y="1554.060198" justify="center" valign="top" font-size="14">Подзаголовок</credit-words>
    </credit>
  <credit page="1">
    <credit-type>composer</credit-type>
    <credit-words default-x="1114.7587" default-y="1511.210312" justify="right" valign="bottom">STN</credit-words>
    </credit>
  <part-list>
    <score-part id="P1">
      <part-name>Piano</part-name>
      <part-abbreviation>Pno.</part-abbreviation>
      <score-instrument id="P1-I1">
        <instrument-name>Piano</instrument-name>
        <instrument-sound>keyboard.piano</instrument-sound>
        </score-instrument>
      <midi-device id="P1-I1" port="1"></midi-device>
      <midi-instrument id="P1-I1">
        <midi-channel>1</midi-channel>
        <midi-program>1</midi-program>
        <volume>78.7402</volume>
        <pan>0</pan>
        </midi-instrument>
      </score-part>
    </part-list>
  <part id="P1">
      <measure number="1" width="251.04">
      <print>
        <system-layout>
          <system-margins>
            <left-margin>50</left-margin>
            <right-margin>-0</right-margin>
            </system-margins>
          <top-system-distance>170</top-system-distance>
          </system-layout>
        </print>
      <attributes>
        <divisions>2</divisions>
        <key>
          <fifths>0</fifths>
          </key>
        <time>
          <beats>4</beats>
          <beat-type>4</beat-type>
          </time>
        <clef>
          <sign>G</sign>
          <line>2</line>
          </clef>
        </attributes>"""


    def __init__(self, audio_file):
        self.duration = NoteDefiner(audio_file).notes_dur_definer()
        self.pitch = NoteDefiner(audio_file).pitch_definer()
        self.freqs = FrequencyExtractor(audio_file).extract_frequencies()
        if self.freqs == []:
            self.start_time = None
        else:
            self.start_time = self.freqs[0]['start_time']


    def start_middle_pause_definer(self, start_time):
        start_time = round(start_time, 2)
        if 0.1 <= start_time <= 0.15:
            return [self.pause_definer(0.25), 0.25]

        elif 0.16 <= start_time <= 0.3:
            return [self.pause_definer(0.5), 0.5]

        elif 0.31 <= start_time <= 0.42:
            return [self.pause_definer(0.75), 0.75]

        elif 0.43 <= start_time <= 0.57:
            return [self.pause_definer(1), 1]

        elif 0.58 <= start_time <= 0.89:
            return [self.pause_definer(1.5), 1.5]

        elif 0.9 <= start_time <= 1.25:
            return [self.pause_definer(2), 2]

        elif 1.26 <= start_time <= 1.75:
            return [self.pause_definer(3), 3]

        elif 1.76 <= start_time <= 2.5:
            return [self.pause_definer(4), 4]
        # -------------------------------------
        elif 2.6 <= start_time <= 3.4:
            return [self.pause_definer(4), 4]

        elif True:
            return [self.pause_definer(4), 4]


    def pause_definer(self, beat):
        pause_xml = """
      <note>
        <rest/>
        <duration>1</duration>
        <voice>1</voice>"""
        sixteenth = "<type>16th</type>" \
                    "</note>"
        eighth = "<type>eighth</type>" \
                 "</note>"
        quarter = "<type>quarter</type>" \
                  "</note>"
        half = "<type>half</type>" \
               "</note>"
        if beat == 0.25:
            return pause_xml + sixteenth
        elif beat == 0.5:
            return pause_xml + eighth
        elif beat == 0.75:
            return pause_xml + eighth + pause_xml + sixteenth
        elif beat == 1:
            return pause_xml + quarter
        elif beat == 1.25:
            return pause_xml + quarter + pause_xml + sixteenth
        elif beat == 1.5:
            return pause_xml + quarter + pause_xml + eighth
        elif beat == 1.75:
            return pause_xml + quarter + pause_xml + eighth + pause_xml + sixteenth
        elif beat == 2:
            return pause_xml + half
        elif beat == 2.25:
            return pause_xml + half + pause_xml + sixteenth
        elif beat == 2.5:
            return pause_xml + half + pause_xml + eighth
        elif beat == 2.75:
            return pause_xml + half + pause_xml + eighth + sixteenth
        elif beat == 3:
            return pause_xml + half + pause_xml + quarter
        elif beat == 3.25:
            return pause_xml + half + pause_xml + quarter + pause_xml + sixteenth
        elif beat == 3.5:
            return pause_xml + half + pause_xml + quarter + pause_xml + eighth
        elif beat == 3.75:
            return pause_xml + half + pause_xml + quarter + pause_xml + eighth + pause_xml + sixteenth
        elif beat == 4:
            return pause_xml + \
                   "<type>whole</type>" \
                   "</note>"


    def beat_to_type(self, beat):
        if beat == 0.25:
            return "<type>16th</type>"
        elif beat == 0.5:
            return "<type>eighth</type>"
        elif beat == 1:
            return "<type>quarter</type>"
        elif beat == 2:
            return "<type>half</type>"
        elif beat == 4:
            return "<type>whole</type>"

        elif beat == 0.75:
            return "<type>eighth</type>" \
                   "<dot/>"
        elif beat == 1.5:
            return "<type>quarter</type>" \
                   "<dot/>"
        elif beat == 3:
            return "<type>half</type>" \
                   "<dot/>"

    def create_mxml(self):
        if self.start_time is None:
            return False
        xml_body = ""
        measure = 1
        num_of_beats = 0

        # Если время начала звучания первой ноты больше 0.05 секунд, то поместить паузу в начало
        if self.start_time > 0.05:
            num_of_beats = num_of_beats + self.start_middle_pause_definer(self.start_time)[1]
            xml_body = str(self.start_middle_pause_definer(self.start_time)[0])

        # ----------------------Цикл по всем нотам, кроме последней--------------------
        for i in range(len(self.pitch) - 1):
            if num_of_beats == 4:
                num_of_beats = 0
                measure += 1
                xml_body = xml_body + f"""
    </measure>
  <measure number="{measure}">"""

            # Если Высота ноты равна или больше выосты ноты B4, то опустить штиль вниз
            if self.pitch[i][:2] == "B4" or int(self.pitch[i][1]) > 4:
                stem = "down"
            else:
                stem = "up"

            # Проверка на диез
            if self.pitch[i][-1] == "#":
                num_of_beats = num_of_beats + self.duration[i]
                xml_body = xml_body + f"""
      <note>
        <pitch>
          <step>{self.pitch[i][0]}</step>
          <alter>1</alter>
          <octave>{self.pitch[i][1]}</octave>
          </pitch>
        <duration>1</duration>
        <voice>1</voice>
        {self.beat_to_type(self.duration[i])}
        <accidental>sharp</accidental>
        <stem>{stem}</stem>
        </note>"""
            else:
                num_of_beats = num_of_beats + self.duration[i]
                xml_body = xml_body + f"""
      <note>
        <pitch>
          <step>{self.pitch[i][0]}</step>
          <octave>{self.pitch[i][1]}</octave>
          </pitch>
        <duration>1</duration>
        <voice>1</voice>
        {self.beat_to_type(self.duration[i])}
        <stem>{stem}</stem>
        </note>"""
            # ---------------------Проверки пауз-------------------------------
            pause = self.freqs[i+1]['start_time'] - self.freqs[i]['start_time'] - self.freqs[i]['duration']
            # Проверка на паузу между соседними нотами
            if pause > 0.2:
                num_of_beats = num_of_beats + self.start_middle_pause_definer(pause)[1]
                xml_body = xml_body + self.start_middle_pause_definer(pause)[0]
                # Если количество четвертей больше 4, то поместить паузу на конец такта
            if num_of_beats + self.duration[i + 1] > 4:
                measure += 1
                type = self.pause_definer(4 - num_of_beats)
                num_of_beats = 0
                xml_body = xml_body + f"""
        {type}
      </measure>
    <measure number="{measure}">"""

        # --------------------------Проверки для последней ноты--------------------------------
        if self.pitch[len(self.pitch) - 1][:2] == "B4" or int(self.pitch[len(self.pitch) - 1][1]) > 4:
            stem = "down"
        else:
            stem = "up"
        if self.pitch[len(self.pitch) - 1][-1] == "#":
            num_of_beats = num_of_beats + self.duration[len(self.pitch) - 1]
            xml_body = xml_body + f"""
      <note>
        <pitch>
          <step>{self.pitch[len(self.pitch) - 1][0]}</step>
          <alter>1</alter>
          <octave>{self.pitch[len(self.pitch) - 1][1]}</octave>
          </pitch>
        <duration>1</duration>
        <voice>1</voice>
        {self.beat_to_type(self.duration[len(self.pitch) - 1])}
        <accidental>sharp</accidental>
        <stem>{stem}</stem>
        </note>"""
        else:
            num_of_beats = num_of_beats + self.duration[len(self.pitch) - 1]
            xml_body = xml_body + f"""
      <note>
        <pitch>
          <step>{self.pitch[len(self.pitch) - 1][0]}</step>
          <octave>{self.pitch[len(self.pitch) - 1][1]}</octave>
          </pitch>
        <duration>1</duration>
        <voice>1</voice>
        {self.beat_to_type(self.duration[len(self.pitch) - 1])}
        <stem>{stem}</stem>
        </note>"""

        # Если такт не завершён, то поместить паузу на конец
        if num_of_beats < 4:
            type = self.pause_definer(4 - num_of_beats)
            xml_body = xml_body + f"""
      {type}
    </measure>
  </part>
</score-partwise>"""
        else:
            xml_body = xml_body + f"""
    </measure>
  </part>
</score-partwise>"""

        return self.file_head + xml_body
