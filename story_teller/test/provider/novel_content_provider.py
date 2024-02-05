from story_teller.model.novel_content import NovelContent, StyleInfo


def create_simple_novel_content():
    return NovelContent(
        title="The journey to the Tower of Light",
        subtitle="A mythical journey of Paul from the City of Darkness to the Tower of Light",
        details="""
Paul was born in the city of darkness, but lost his parents in a terrible accident. As an orphan he survided with the help of some other children which also formed a gang.
However the situation in the city of darkness kept worsening, so that Paul and his friends decided to flee from it = a daunting and perilous task. The City of Darkness was 
a kind of prison in which the Zorr, the Dark Tyrant rules with an iron fist. The idea of the Tower of Light was based on ancient legends, but gives Paul and hist friends 
hope for a better light. Paul will travel through the Desert of Snakes, the Mines of Despair, the Swamp of Doubt and finally the Land of the Storms to reach the mysterious 
Tower of Light. He will have three friends with him, but will ultimately be victorious.
""",
        style_info=StyleInfo(author="Tolkien", book="Lord of the Rings"),
    )


def create_simple_novel_content_2():
    return NovelContent(
        title="The Three Rivers",
        subtitle="Calypso's Odyssee to the City of Amber",
        details="""
Calypso is a young woman who lives a happy life in her village. One day whilst she was going home from her work in the fields, she meets an old woman, she never saw before. 
This woman tells her that only after losing everything, her wishes will be fulfilled and that she needs to traverse the 3 rivers. Calypso finds this weird, but she gets no further explanation for the woman's remarks.
The woman disappears after that to never be seen again and Calypso forgets about the incident.
A couple of days later a devastating storm destroys her village, Callypso loses everything, her family, her house, her job. Only two kids she knows and a dog are rescued in the after
Calypso remembers now the old woman and what she said. She decides to take whatever she has and to look for the three rivers to traverse them and siscover what lies beyond.
She will reach the three rivers after lots of adventures, discover the identity of the old woman and finally reach the City of Amber with the two kids and the dog where she will start a new life.
""",
        style_info=StyleInfo(author="Tolkien", book="Lord of the Rings"),
    )


def create_simple_novel_content_3():
    return NovelContent(
        title="The Eight Chambers",
        subtitle="Jonathan And The Eight Chambers",
        details="""
Jonathan was a servant in the distant kingdom from Afar. Even though his life was one of hard labour and hardships under the rule of King Thorn the Third, Jonathan was a visionary man. 
During the late Summer months after the harvest he regularly would have the vision of an angel which would tell him about the Eight chambers that he needed to open. Every year he would mention one chamber.
Every vision would be dedicated to one chamber. The first chamber was the chamber of introspection and silence. Theh second chamber the chamber of the victory over distractions and fear, the
third the chamber of flexibility and the wisdom to adapt, the fourth the chamber of tolerance to hardships and suffering, the fifth, the chamber of clear vision and discernment, the sixth, 
the chamber of judgement and decisiveness and the seventh, the chamber of courage and confrontation in which he needed to put everything he learnt into practice. And finally there was the last chamber, the chamber of compassion and service to mankind.

It so happened that after the last vision about the Eighth Chamber, a tremendous war started in King Thorn's Kingdom. During the siege of Thorn's castle, Jonathan accessed the Thorn's hidden dungeons during the whole chaos and 
got lost in the dungeon's maze. It is int this maze that Jonathan will find the chambers one by one. The last chamber however will allow Jonathan to escape from all the chaos and oppressive Kingdom of Thorn. 
The last chamber represents the beginning of a new life for Jonathan in a new World of freedom and peace.
""",
        style_info=StyleInfo(author="Tolkien", book="Lord of the Rings"),
    )
