from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from study.models import Deck, Card
from django.utils import timezone
from datetime import timedelta
import random

class Command(BaseCommand):
    help = 'Seeds the database with a demo user, decks, and cards.'

    def handle(self, *args, **kwargs):
        # Create demo user as superuser so they can access the admin panel
        user, created = User.objects.get_or_create(username='demo_admin', email='demo@example.com')
        user.is_staff = True
        user.is_superuser = True
        if created:
            user.set_password('demo1234')
        user.save()
        if created:
            self.stdout.write(self.style.SUCCESS('Successfully created demo user (demo_admin / demo1234) as Admin.'))
        else:
            self.stdout.write(self.style.WARNING('Demo user already exists. Upgraded to Admin.'))
            # Delete existing decks for a fresh start
            Deck.objects.filter(owner=user).delete()

        # Create decks
        decks_data = [
            {
                "title": "IELTS Academic Vocabulary",
                "subject": "LANGUAGE",
                "desc": "Essential vocabulary for IELTS Academic.",
                "cards": [
                    {"front": "Ubiquitous (adj.)", "back": "Present, appearing, or found everywhere.", "hint": "Synonym: Omnipresent"},
                    {"front": "Mitigate (v.)", "back": "Make less severe, serious, or painful.", "hint": "Synonym: Alleviate"},
                    {"front": "Pragmatic (adj.)", "back": "Dealing with things sensibly and realistically.", "hint": "Synonym: Practical"},
                    {"front": "Anomalous (adj.)", "back": "Deviating from what is standard, normal, or expected.", "hint": "Synonym: Abnormal"},
                    {"front": "Cacophony (n.)", "back": "A harsh, discordant mixture of sounds.", "hint": "Think of a noisy city street"},
                    {"front": "Ephemeral (adj.)", "back": "Lasting for a very short time.", "hint": "Synonym: Fleeting"},
                    {"front": "Lethargic (adj.)", "back": "Sluggish and apathetic.", "hint": "Synonym: Inactive"},
                    {"front": "Meticulous (adj.)", "back": "Showing great attention to detail; very careful.", "hint": "Synonym: Thorough"},
                    {"front": "Obscure (adj.)", "back": "Not discovered or known about; uncertain.", "hint": "Synonym: Unclear"},
                    {"front": "Prolific (adj.)", "back": "Producing much fruit or foliage or many offspring.", "hint": "Synonym: Productive"},
                    {"front": "Resilient (adj.)", "back": "Able to withstand or recover quickly from difficult conditions.", "hint": "Synonym: Strong"},
                    {"front": "Superfluous (adj.)", "back": "Unnecessary, especially through being more than enough.", "hint": "Synonym: Extra"},
                    {"front": "Tenacious (adj.)", "back": "Tending to keep a firm hold of something; clinging.", "hint": "Synonym: Persistent"},
                    {"front": "Venerate (v.)", "back": "Regard with great respect; revere.", "hint": "Synonym: Worship"},
                    {"front": "Zealous (adj.)", "back": "Showing great energy or enthusiasm in pursuit of a cause or an objective.", "hint": "Synonym: Passionate"},
                    {"front": "Abstain (v.)", "back": "Restrain oneself from doing or enjoying something.", "hint": "Synonym: Refrain"},
                    {"front": "Capricious (adj.)", "back": "Given to sudden and unaccountable changes of mood or behavior.", "hint": "Synonym: Fickle"},
                    {"front": "Lucid (adj.)", "back": "Expressed clearly; easy to understand.", "hint": "Synonym: Clear"},
                    {"front": "Placate (v.)", "back": "Make (someone) less angry or hostile.", "hint": "Synonym: Pacify"},
                    {"front": "Sagacious (adj.)", "back": "Having or showing keen mental discernment and good judgment.", "hint": "Synonym: Wise"}
                ]
            },
            {
                "title": "IELTS Speaking Topics",
                "subject": "INTERVIEW",
                "desc": "Common speaking topics and phrases.",
                "cards": [
                    {"front": "Describe a memorable journey you have made.", "back": "I would like to talk about a trip I took to... The most memorable part was... It left a lasting impression on me because...", "hint": "Part 2 Cue Card"},
                    {"front": "What are the advantages of living in a city?", "back": "Well, cities offer a plethora of opportunities, such as better infrastructure, diverse career prospects, and access to top-tier healthcare.", "hint": "Part 3 Discussion"},
                    {"front": "How do you usually spend your weekends?", "back": "Typically, I prefer to unwind by reading a book or catching up with friends over coffee. It helps me recharge for the week ahead.", "hint": "Part 1 Introduction"},
                    {"front": "Phrase for introducing an opposing view", "back": "On the other hand...", "hint": "Linking word"},
                    {"front": "Phrase for giving an example", "back": "For instance... / A prime example of this would be...", "hint": "Linking word"},
                    {"front": "Describe a person who has influenced you significantly.", "back": "The person I'd like to describe is my... They had a profound impact on my life by teaching me...", "hint": "Part 2 Cue Card"},
                    {"front": "Do you think technology has made our lives better?", "back": "Undoubtedly, technology has revolutionized the way we live and work, making tasks more efficient, though it does come with drawbacks like screen fatigue.", "hint": "Part 3 Discussion"},
                    {"front": "What kind of music do you enjoy listening to?", "back": "I'm quite fond of classical music. I find it incredibly soothing and it helps me concentrate when I'm working.", "hint": "Part 1 Introduction"},
                    {"front": "Phrase for expressing strong agreement", "back": "I completely agree with that perspective. / I couldn't agree more.", "hint": "Opinion phrase"},
                    {"front": "Phrase for concluding a point", "back": "To sum up... / Ultimately, what it boils down to is...", "hint": "Linking word"}
                ]
            },
            {
                "title": "English Idioms",
                "subject": "LANGUAGE",
                "desc": "Common idioms for native-like fluency.",
                "cards": [
                    {"front": "A blessing in disguise", "back": "A good thing that seemed bad at first.", "hint": "Think of hidden good"},
                    {"front": "Bite the bullet", "back": "To force yourself to do something unpleasant or difficult.", "hint": "Enduring pain"},
                    {"front": "Call it a day", "back": "To stop what you are doing because you think you have done enough or do not want to do any more.", "hint": "Ending work"},
                    {"front": "Cut corners", "back": "To do something perfunctorily so as to save time or money.", "hint": "Taking shortcuts"},
                    {"front": "Get out of hand", "back": "Get out of control.", "hint": "Losing grip"},
                    {"front": "Hit the nail on the head", "back": "To describe exactly what is causing a situation or problem.", "hint": "Precision"},
                    {"front": "Let the cat out of the bag", "back": "To share information that was previously concealed.", "hint": "Revealing a secret"},
                    {"front": "Miss the boat", "back": "To be too late to get something that you want.", "hint": "Losing an opportunity"},
                    {"front": "On the ball", "back": "Alert to new ideas, methods, and trends.", "hint": "Being focused"},
                    {"front": "Under the weather", "back": "Slightly unwell or in low spirits.", "hint": "Feeling sick"}
                ]
            }
        ]

        # Process decks and cards
        now = timezone.now()
        intervals = {1: 0, 2: 1, 3: 3, 4: 7, 5: 16}
        cards_created = 0

        for d_data in decks_data:
            deck = Deck.objects.create(
                owner=user,
                title=d_data["title"],
                description=d_data["desc"],
                subject=d_data["subject"]
            )
            
            for item in d_data["cards"]:
                box = random.randint(1, 5)
                # Some cards due today, some in the future, some past
                due_offset = random.randint(-2, intervals[box])
                next_review = now + timedelta(days=due_offset)
                
                Card.objects.create(
                    deck=deck,
                    front=item["front"],
                    back=item["back"],
                    hint=item["hint"],
                    box=box,
                    next_review_at=next_review,
                    last_reviewed_at=now - timedelta(days=1) if box > 1 else None,
                    times_reviewed=box * 2,
                    times_correct=box * 2 - 1 if box > 1 else 0
                )
                cards_created += 1

        self.stdout.write(self.style.SUCCESS(f'Successfully seeded {len(decks_data)} decks and {cards_created} cards.'))
