import random
from datetime import timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.contrib.auth.models import User
from study.models import Deck, Card

class Command(BaseCommand):
    help = 'Seeds the database with a demo user, decks, and cards (100 per category).'

    def handle(self, *args, **kwargs):
        # Create admin user for admin panel
        admin, created = User.objects.get_or_create(username='admin')
        admin.email = 'admin@example.com'
        admin.is_staff = True
        admin.is_superuser = True
        admin.set_password('admin123')
        admin.save()

        # Create demo user as standard user
        user, created = User.objects.get_or_create(username='demo')
        user.email = 'demo@example.com'
        user.is_staff = False
        user.is_superuser = False
        user.set_password('demo123')
        user.save()
        
        self.stdout.write(self.style.WARNING('Clearing existing decks for demo user...'))
        Deck.objects.filter(owner=user).delete()

        # Content bases (20 items each)
        prog_base = [
            ("What is Polymorphism?", "The ability of different classes to respond to the same method call in their own way."),
            ("Define Encapsulation.", "Bundling data and methods that operate on that data within a single unit or class."),
            ("What is a Closure?", "A function that retains access to its lexical scope, even when executed outside of it."),
            ("Explain REST.", "Representational State Transfer; an architectural style for designing networked applications."),
            ("What is the Virtual DOM?", "A lightweight JavaScript representation of the actual DOM used by React for performance."),
            ("What is a Promise?", "An object representing the eventual completion or failure of an asynchronous operation."),
            ("Define SQL Injection.", "A web security vulnerability that allows an attacker to interfere with database queries."),
            ("What is Git Rebase?", "Moving or combining a sequence of commits to a new base commit."),
            ("Explain Big O Notation.", "Mathematical notation that describes the limiting behavior of a function (time/space complexity)."),
            ("What is a Hash Table?", "A data structure that implements an associative array abstract data type using a hash function."),
            ("What is CSS Flexbox?", "A one-dimensional layout method for arranging items in rows or columns."),
            ("Define Middleware.", "Software that bridges gaps between other applications, tools, and databases."),
            ("What is an API?", "Application Programming Interface; a set of rules allowing different software entities to communicate."),
            ("What is JWT?", "JSON Web Token; a compact, URL-safe means of representing claims to be transferred between two parties."),
            ("Explain MVC.", "Model-View-Controller; a software design pattern for developing user interfaces."),
            ("What is Docker?", "A platform designed to help developers build, share, and run modern applications using containers."),
            ("What is a Webhook?", "A method of augmenting or altering the behavior of a web page or web application with custom callbacks."),
            ("Define Microservices.", "An architectural style that structures an application as a collection of loosely coupled services."),
            ("What is CORS?", "Cross-Origin Resource Sharing; a mechanism that allows restricted resources to be requested from another domain."),
            ("Explain GraphQL.", "A query language for APIs and a runtime for fulfilling those queries with existing data.")
        ]

        lang_base = [
            ("Ubiquitous (adj.)", "Present, appearing, or found everywhere."),
            ("Mitigate (v.)", "Make less severe, serious, or painful."),
            ("Pragmatic (adj.)", "Dealing with things sensibly and realistically."),
            ("Anomalous (adj.)", "Deviating from what is standard, normal, or expected."),
            ("Cacophony (n.)", "A harsh, discordant mixture of sounds."),
            ("Ephemeral (adj.)", "Lasting for a very short time."),
            ("Lethargic (adj.)", "Sluggish and apathetic."),
            ("Meticulous (adj.)", "Showing great attention to detail; very careful."),
            ("Obscure (adj.)", "Not discovered or known about; uncertain."),
            ("Prolific (adj.)", "Producing much fruit or foliage or many offspring."),
            ("Resilient (adj.)", "Able to withstand or recover quickly from difficult conditions."),
            ("Superfluous (adj.)", "Unnecessary, especially through being more than enough."),
            ("Tenacious (adj.)", "Tending to keep a firm hold of something; clinging."),
            ("Venerate (v.)", "Regard with great respect; revere."),
            ("Zealous (adj.)", "Showing great energy or enthusiasm in pursuit of a cause or an objective."),
            ("Abstain (v.)", "Restrain oneself from doing or enjoying something."),
            ("Capricious (adj.)", "Given to sudden and unaccountable changes of mood or behavior."),
            ("Lucid (adj.)", "Expressed clearly; easy to understand."),
            ("Placate (v.)", "Make (someone) less angry or hostile."),
            ("Sagacious (adj.)", "Having or showing keen mental discernment and good judgment.")
        ]

        acad_base = [
            ("Photosynthesis", "Process by which green plants use sunlight to synthesize nutrients from CO2 and water."),
            ("Mitochondria", "An organelle found in large numbers in most cells, in which respiration and energy production occur."),
            ("Newton's First Law", "An object at rest stays at rest and an object in motion stays in motion unless acted upon by a net external force."),
            ("Pythagorean Theorem", "a² + b² = c² in a right-angled triangle."),
            ("Quantum Entanglement", "A physical phenomenon that occurs when pairs or groups of particles are generated or interact in ways such that the quantum state of each particle cannot be described independently."),
            ("Avogadro's Number", "6.022 × 10²³; the number of constituent particles that are contained in one mole of a given substance."),
            ("Fibonacci Sequence", "A series of numbers in which each number is the sum of the two preceding ones."),
            ("Plate Tectonics", "A theory explaining the structure of the earth's crust and many associated phenomena."),
            ("Natural Selection", "The process whereby organisms better adapted to their environment tend to survive and produce more offspring."),
            ("Atomic Number", "The number of protons in the nucleus of an atom, which determines the chemical properties of an element."),
            ("Law of Conservation of Mass", "Mass is neither created nor destroyed in chemical reactions."),
            ("Thermodynamics (2nd Law)", "The total entropy of an isolated system can never decrease over time."),
            ("DNA (Deoxyribonucleic Acid)", "A self-replicating material present in nearly all living organisms as the main constituent of chromosomes."),
            ("Mitosis", "A type of cell division that results in two daughter cells each having the same number and kind of chromosomes as the parent nucleus."),
            ("Osmosis", "A process by which molecules of a solvent tend to pass through a semipermeable membrane from a less concentrated solution into a more concentrated one."),
            ("Kinetic Energy", "Energy that a body possesses by virtue of being in motion."),
            ("Electromagnetic Spectrum", "The range of wavelengths or frequencies over which electromagnetic radiation extends."),
            ("Heisenberg Uncertainty Principle", "It is impossible to know both the exact position and the exact velocity of an object at the same time."),
            ("Tectonic Uplift", "Geological process most often caused by plate tectonics which increases elevation."),
            ("Isotopes", "Two or more forms of the same element that contain equal numbers of protons but different numbers of neutrons.")
        ]

        int_base = [
            ("Tell me about yourself.", "Focus on professional background, key achievements, and current goals."),
            ("What is your greatest weakness?", "Mention a real weakness and how you are actively working to improve it."),
            ("Where do you see yourself in 5 years?", "Align personal goals with the company's trajectory and role progression."),
            ("Why do you want to work here?", "Highlight specific company values, products, or culture that resonate with you."),
            ("Describe a time you overcame a challenge.", "Use the STAR method: Situation, Task, Action, Result."),
            ("Why should we hire you?", "Summarize unique skills and cultural fit that directly solve their problems."),
            ("What is your greatest achievement?", "Discuss a professional milestone with quantifiable results."),
            ("How do you handle conflict at work?", "Emphasize communication, empathy, and focusing on professional resolutions."),
            ("What are your salary expectations?", "Provide a well-researched range based on market value and flexibility."),
            ("Do you have any questions for us?", "Ask insightful questions about team dynamics, challenges, or company vision."),
            ("How do you prioritize tasks?", "Discuss time management tools and evaluating urgency vs. importance."),
            ("Describe your leadership style.", "Focus on collaboration, delegation, and supporting team members."),
            ("What motivates you?", "Mention learning, impact, solving complex problems, or team success."),
            ("How do you handle failure?", "Frame it as a learning opportunity; describe taking accountability and adapting."),
            ("Why are you leaving your current job?", "Keep it positive: seeking new challenges, growth, or alignment with goals."),
            ("What is your working style?", "Describe adaptability, communication preferences, and independent vs. team work."),
            ("How do you deal with pressure?", "Mention staying calm, breaking down tasks, and seeking support if needed."),
            ("Describe a time you disagreed with a manager.", "Focus on respectful dialogue, data-driven points, and committing to the final decision."),
            ("What are you passionate about?", "Connect personal passions to professional drive and continuous learning."),
            ("What makes you unique?", "Highlight a combination of soft and hard skills that sets you apart.")
        ]

        oth_base = [
            ("Capital of Australia", "Canberra"),
            ("Tallest mountain in the world", "Mount Everest"),
            ("Author of '1984'", "George Orwell"),
            ("Chemical symbol for Gold", "Au"),
            ("Largest ocean on Earth", "Pacific Ocean"),
            ("Year World War II ended", "1945"),
            ("First human in space", "Yuri Gagarin"),
            ("Painter of the Mona Lisa", "Leonardo da Vinci"),
            ("Hardest natural mineral", "Diamond"),
            ("Largest planet in our solar system", "Jupiter"),
            ("Currency of Japan", "Yen"),
            ("Longest river in the world", "Nile (or Amazon, depending on the metric)"),
            ("Inventor of the Telephone", "Alexander Graham Bell"),
            ("Smallest country in the world", "Vatican City"),
            ("Main ingredient in Guacamole", "Avocado"),
            ("Fastest land animal", "Cheetah"),
            ("Number of continents", "Seven"),
            ("Capital of Canada", "Ottawa"),
            ("Primary language of Brazil", "Portuguese"),
            ("Author of 'Harry Potter'", "J.K. Rowling")
        ]

        # Expand to 100 items by adding variations
        def expand_to_100(base_list, prefix=""):
            expanded = []
            for i in range(5):
                for q, a in base_list:
                    mod = f" [Set {i+1}]" if i > 0 else ""
                    expanded.append((f"{prefix}{q}{mod}", a))
            return expanded

        decks_data = [
            {"title": "Software Engineering 101", "subject": "PROGRAMMING", "desc": "100 crucial concepts.", "cards": expand_to_100(prog_base)},
            {"title": "IELTS Academic Vocabulary", "subject": "LANGUAGE", "desc": "100 essential words.", "cards": expand_to_100(lang_base)},
            {"title": "Science & Math Core", "subject": "ACADEMIC", "desc": "100 fundamental truths.", "cards": expand_to_100(acad_base)},
            {"title": "Behavioral Interviews", "subject": "INTERVIEW", "desc": "100 prep scenarios.", "cards": expand_to_100(int_base)},
            {"title": "World Trivia", "subject": "OTHER", "desc": "100 random facts.", "cards": expand_to_100(oth_base)}
        ]

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
            
            for front, back in d_data["cards"]:
                box = random.randint(1, 5)
                due_offset = random.randint(-2, intervals[box])
                next_review = now + timedelta(days=due_offset)
                
                Card.objects.create(
                    deck=deck,
                    front=front,
                    back=back,
                    hint=f"Subject: {d_data['subject']}",
                    box=box,
                    next_review_at=next_review,
                    last_reviewed_at=now - timedelta(days=1) if box > 1 else None,
                    times_reviewed=box * 2,
                    times_correct=box * 2 - 1 if box > 1 else 0
                )
                cards_created += 1

        self.stdout.write(self.style.SUCCESS(f'Successfully seeded {len(decks_data)} decks and {cards_created} cards.'))
