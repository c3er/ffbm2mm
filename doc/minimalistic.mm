<map version="freeplane 1.2.0">
<!--
    How simple can a Freeplane mind map file be and still be valid?
    
    Needed:
    - Node structure
    - Node labels
    - Containing links
    
    Notes:
    - The root node needs a version attribute. It was tried to give this version
      a lowest number as possible.
-->
<node TEXT="Test">
<node TEXT="Das ist ein Test"/>
<node TEXT="Noch ein Test"/>
<node TEXT="Ein Link" LINK="https://docs.python.org/3.5/library/json.html"/>
<node TEXT="https://docs.python.org/3.5/library/json.html" LINK="https://docs.python.org/3.5/library/json.html"/>
<node TEXT="https://www.google.de/" LINK="https://www.google.de/">
<node TEXT="Direkte Adreese und mit Kind"/>
</node>
<node TEXT="http://effbot.org/tkinterbook/button.htm" LINK="http://effbot.org/tkinterbook/button.htm"/>
<node TEXT="Jetzt mit Hierarchie">
<node TEXT="1. Kind"/>
<node TEXT="2. Kind">
<node TEXT="1. Kindkind">
<node TEXT="Kindkindkind"/>
</node>
<node TEXT="2. Kindkind"/>
</node>
<node TEXT="3. Kind"/>
</node>
</node>
</map>
