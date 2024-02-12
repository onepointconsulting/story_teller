from pathlib import Path
from story_teller.model.developed_chapter import DevelopedChapter
from story_teller.test.provider.novel_content_provider import (
    create_simple_novel_content_3,
)


def create_sample_chapter_content():
    return """
1. Chapter One: The City of Shadows
   - Paul's life in the City of Darkness
   - The loss of his parents
   - Survival with the gang of orphans

2. Chapter Two: The Tyranny of Zorr
   - Daily life under Zorr's rule
   - The decision to escape
   - Preparations for the perilous journey

3. Chapter Three: Into the Desert of Snakes
   - The beginning of Paul and his friends' journey
   - Encounters with the dangers of the desert
   - Camaraderie and first tests of their resolve

4. Chapter Four: The Mines of Despair
   - Delving into the dark and treacherous mines
   - Struggles and challenges underground
   - Discovering strengths they never knew they had

5. Chapter Five: The Swamp of Doubt
   - Navigating the deceiving paths of the swamp
   - Overcoming personal fears and insecurities
   - The power of hope and belief in the legend

6. Chapter Six: The Land of the Storms
   - Braving the fierce elements in the final stretch
   - Moments of despair and thoughts of giving up
   - The final battle against the storm and themselves

7. Chapter Seven: The Tower of Light
   - The awe-inspiring sight of the Tower of Light
   - Reflections on the journey and its hardships
   - The climax of Paul's quest and the new beginning
"""


def create_developed_chapter() -> DevelopedChapter:
    novel_content = create_simple_novel_content_3()
    return DevelopedChapter(
        sequence=1,
        name="Jonathan and The Chamber of Introspection and Silence",
        description="Jonathan begins his arduous journey by entering the first chamber, where he must face his own thoughts and learn the virtue of stillness.",
        content="""
In the bowels of Thorn's castle, the echo of war's cacophony raged above, the ground beneath Jonathan's feet trembled with the fury of the besieging forces. Here, the air was thick with the dust of ancient stones, and the darkness was a tangible shroud around him. His hands brushed against the cold, damp walls as he navigated the labyrinthine passages, a serendipitous path that led him to the first of the eight chambers: the Chamber of Introspection and Silence.

As he stepped through the stone archway, a sudden hush enveloped him, a silence so profound it seemed to swallow even the beat of his own heart. The chamber was austere, lit only by the slivers of light that crept in through narrow fissures in the ceiling, casting a spectral dance upon the walls.

Here, in the solitude of his own mind, Jonathan found himself alone with his thoughts, a cacophony more raucous than the war above. They were the thoughts of years of servitude, of dreams suppressed, of a life lived in the shadows of King Thorn's oppressive reign. Yet, the angel's words, an ethereal whisper, beckoned him to embrace the stillness, to listen not to the noise, but to the silence between.

In the silence, Jonathan's breath became his anchor, each inhale a surge of life, each exhale a release of the burdens he carried. Memories unfolded before him, not as torturous specters to flee from, but as moments to be observed, acknowledged, and understood. He saw his hands, roughened by toil, and recognized the strength that hardship had forged within them. He saw his heart, wearied by sorrow, and yet still capable of hope.

Hours slipped into eternity within the chamber. Jonathan felt the remnants of his old self - the fears, the doubts, the unyielding grip of the past - begin to dissipate. The virtue of stillness was not inaction; it was the deliberate calm at the center of the storm, the eye where one could see with clarity the tumult of life without being swept away by it.

In this chamber, Jonathan was both the prisoner and the warden, the one who could set himself free. The silence was not a void, but a canvas, vast and infinite, upon which he could begin to paint the vision of the man he yearned to become. It was here that he learned to listen to the quiet wisdom of his own spirit, to the voice that had been drowned out by the clamor of the world.

As the silence deepened, Jonathan found within it a profound truth: that freedom was not a distant land to be reached, but a state of being to be cultivated within the confines of one's own mind. It was the first key, the first step on the arduous journey toward the final chamber and the promise of a new life that lay beyond.

When at last he rose from the stone floor, his limbs stiff from the passage of unmarked time, Jonathan felt a newfound resolve crystallize within him. He was ready to face the remaining chambers, each with its own trial, its own lesson to impart.

The Chamber of Introspection and Silence had been a crucible, and from its depths, Jonathan emerged not unscathed, but transformed. He stepped back into the maze, the echoes of war a faint reminder of a world he was learning to transcend, a world he would one day leave behind.

As he walked away, his footsteps were measured and deliberate, each one a testament to the stillness he now carried within. The chamber had been a mirror, reflecting back at him not just the man he was, but the man he could become. And in that reflection, Jonathan found the first stirrings of freedom.

In this chapter we are capturing the style of Hemigway using his colourful and metaphorical language.
""",
        image_location=Path("/tmp/test.png"),
        novel_content=novel_content,
    )
