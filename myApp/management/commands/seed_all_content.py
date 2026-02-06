from django.core.management.base import BaseCommand
from myApp.models import (
    HeroSection, CredibilitySection, CredibilityCard,
    TestimonialsSection, Testimonial, StatisticsSection,
    PainPointsSection, MethodologySection, MethodologyStep,
    AboutSection, MissionVisionSection, LeadMagnetSection,
    FinalCTASection
)

class Command(BaseCommand):
    help = 'Seed all content sections with initial data from templates'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting to seed all content sections...\n'))
        
        # 1. Hero Section
        hero = HeroSection.get_instance()
        hero.title = "Stop Losing Money to Property Managers Who Don't Care."
        hero.subtitle = "Your Investment Deserves an Owner's Standard."
        hero.description = "Most property management firms treat you like another number. At Garden Gate, you work directly with me – Mahrukh Tariq. I manage your property with the same standards I apply to my own 90-unit portfolio: honest pricing, rigorous tenant screening, and personal attention that corporations can't replicate."
        hero.cta_text = "Find Out If We're the Right Fit"
        hero.cta_link = "#consultation"
        hero.save()
        self.stdout.write(self.style.SUCCESS('✓ Seeded: Hero Section'))
        
        # 2. Credibility Section
        credibility = CredibilitySection.get_instance()
        credibility.title = "Proven Experience. Personal Commitment.<br>Real Results."
        credibility.description = "Garden Gate is not a franchise or volume-driven agency. It's a boutique property management firm built on 13 years of hands-on real estate experience — backed by a personal portfolio that proves its systems deliver results."
        credibility.subtitle = "Why Landlords Choose Garden Gate"
        credibility.subtitle_description = "Most property managers have never been landlords. Mahrukh Tariq is both. Here's why that matters to your bottom line:"
        credibility.save()
        self.stdout.write(self.style.SUCCESS('✓ Seeded: Credibility Section Header'))
        
        # Credibility Cards (4 cards - using placeholder content from template, will need to be updated)
        credibility_cards_data = [
            {
                'card_number': 1,
                'title': 'Personal Tenant Screening',
                'description': 'With an average 4-day placement time, vacancies are filled faster than competitors who sit empty for weeks. Experience as a landlord ensures speed without compromising quality.'
            },
            {
                'card_number': 2,
                'title': 'Personal Tenant Screening',
                'description': 'With an average 4-day placement time, vacancies are filled faster than competitors who sit empty for weeks. Experience as a landlord ensures speed without compromising quality.'
            },
            {
                'card_number': 3,
                'title': 'Personal Tenant Screening',
                'description': 'With an average 4-day placement time, vacancies are filled faster than competitors who sit empty for weeks. Experience as a landlord ensures speed without compromising quality.'
            },
            {
                'card_number': 4,
                'title': 'Personal Tenant Screening',
                'description': 'With an average 4-day placement time, vacancies are filled faster than competitors who sit empty for weeks. Experience as a landlord ensures speed without compromising quality.'
            },
        ]
        
        for data in credibility_cards_data:
            card, created = CredibilityCard.objects.update_or_create(
                card_number=data['card_number'],
                defaults=data
            )
            self.stdout.write(self.style.SUCCESS(f'  ✓ {"Created" if created else "Updated"}: Credibility Card {card.card_number}'))
        
        # 3. Testimonials Section
        testimonials_section = TestimonialsSection.get_instance()
        testimonials_section.title = "Why Landlords Stop Looking After Finding Us"
        testimonials_section.cta_text = "Find Out If We're the Right Fit"
        testimonials_section.cta_link = "#consultation"
        testimonials_section.save()
        self.stdout.write(self.style.SUCCESS('✓ Seeded: Testimonials Section Header'))
        
        # Testimonials (3 testimonials)
        testimonials_data = [
            {
                'testimonial_number': 1,
                'avatar_url': 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=100&h=100&fit=crop&q=80',
                'avatar_alt': 'Tom R.',
                'quote_short': "After three property managers, I finally found someone who answers the phone.",
                'quote_long': "I wasted two years with managers who'd take 3 days to return a call if they called back at all. With Mahrukh, if something comes up at 8 PM, she responds. That level of access is exactly what I needed.",
                'author_name': 'Tom R.',
                'author_title': '3 properties in Alexandria'
            },
            {
                'testimonial_number': 2,
                'avatar_url': 'https://images.unsplash.com/photo-1438761681033-6461ffad8d80?w=100&h=100&fit=crop&q=80',
                'avatar_alt': 'Jennifer M.',
                'quote_short': "She rented my vacant property in 4 days. Others took 6 weeks.",
                'quote_long': "I had five comparable units listed at the same time through different managers. Mine was the only one that rented fast, because Mahrukh prices right and pre-screens aggressively. Every day vacant was costing me $120. She just made me $3,360.",
                'author_name': 'Jennifer M.',
                'author_title': 'Fairfax investor'
            },
            {
                'testimonial_number': 3,
                'avatar_url': 'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=100&h=100&fit=crop&q=80',
                'avatar_alt': 'David K.',
                'quote_short': "No more surprise $800 invoices I never approved.",
                'quote_long': "My last manager would just bill me for work I didn't authorize. Mahrukh sends estimates for everything over $200. I approve it, THEN the work happens. That's how it should have worked all along.",
                'author_name': 'David K.',
                'author_title': 'Arlington landlord'
            },
        ]
        
        for data in testimonials_data:
            testimonial, created = Testimonial.objects.update_or_create(
                testimonial_number=data['testimonial_number'],
                defaults=data
            )
            self.stdout.write(self.style.SUCCESS(f'  ✓ {"Created" if created else "Updated"}: Testimonial {testimonial.testimonial_number} - {testimonial.author_name}'))
        
        # 4. Statistics Section
        statistics = StatisticsSection.get_instance()
        statistics.title = "Why Quality Management Matters"
        statistics.subtitle = "The Cost of Poor Management:"
        statistics.point_1 = "Long vacancies that cost thousands in lost rent."
        statistics.point_2 = "Vendor markups of 10–25% on maintenance invoices."
        statistics.point_3 = "Unresponsive managers — 29% of tenants report landlords are \"slow to get things done.\""
        statistics.save()
        self.stdout.write(self.style.SUCCESS('✓ Seeded: Statistics Section'))
        
        # 5. Pain Points Section
        pain_points = PainPointsSection.get_instance()
        pain_points.title = "Common Problems.<br>Clear Solutions."
        pain_points.description = "Owning rental property shouldn't mean chasing managers or worrying about surprise bills. But too often, landlords deal with:"
        pain_points.pain_point_1 = "Managers who disappear when you need answers."
        pain_points.pain_point_2 = "Inflated maintenance costs and hidden markups."
        pain_points.pain_point_3 = "Weak screening that lets in problem tenants."
        pain_points.pain_point_4 = "Generic, one-size-fits-all service."
        pain_points.pain_point_5 = "Unapproved expenses with zero transparency."
        pain_points.solution_1 = "<strong class=\"text-gold italic\">Immediate Access</strong> — You call. I answer. Same day."
        pain_points.solution_2 = "<strong class=\"text-gold italic\">Transparent Pricing</strong> — You review every estimate before work begins."
        pain_points.solution_3 = "<strong class=\"text-gold italic\">Rigorous Screening</strong> — Every tenant meets me personally before approval."
        pain_points.solution_4 = "<strong class=\"text-gold italic\">Customized Management</strong> — Your goals, your preferences, your plan."
        pain_points.solution_5 = "<strong class=\"text-gold italic\">Total Transparency</strong> — You're informed before money moves. Always."
        pain_points.cta_text = "Get a Free Rental Analysis"
        pain_points.cta_link = "#consultation"
        pain_points.save()
        self.stdout.write(self.style.SUCCESS('✓ Seeded: Pain Points Section'))
        
        # 6. Methodology Section
        methodology = MethodologySection.get_instance()
        methodology.title = "The Garden Gate Framework"
        methodology.description = "Most companies chase volume. We build relationships. Every property receives personalized attention, open communication, and proactive care."
        methodology.cta_text = "Get a Free Rental Analysis"
        methodology.cta_link = "#consultation"
        methodology.save()
        self.stdout.write(self.style.SUCCESS('✓ Seeded: Methodology Section Header'))
        
        # Methodology Steps (5 steps)
        methodology_steps_data = [
            {
                'step_number': 1,
                'title': 'Assessment',
                'description': "We start with your goals — returns, concerns, and preferences.",
                'result_text': 'Result: A plan that fits you, not a template.'
            },
            {
                'step_number': 2,
                'title': 'Protection',
                'description': 'Thorough screening and in-person showings ensure only the right tenants move in.',
                'result_text': 'Result: Fewer turnovers, more stability.'
            },
            {
                'step_number': 3,
                'title': 'Management',
                'description': 'Rent collection, maintenance, inspections — done right, not rushed.',
                'result_text': 'Result: Lower costs, faster resolutions, lasting peace of mind.'
            },
            {
                'step_number': 4,
                'title': 'Communication',
                'description': "You always reach me directly, no forms, no waiting.",
                'result_text': 'Result: Clear answers. Real accountability.'
            },
            {
                'step_number': 5,
                'title': 'Optimization',
                'description': "We don't just manage; we help your property grow in value.",
                'result_text': 'Result: Competitive rent, increased returns, confident ownership.'
            },
        ]
        
        for data in methodology_steps_data:
            step, created = MethodologyStep.objects.update_or_create(
                step_number=data['step_number'],
                defaults=data
            )
            self.stdout.write(self.style.SUCCESS(f'  ✓ {"Created" if created else "Updated"}: Methodology Step {step.step_number} - {step.title}'))
        
        # 7. About Section
        about = AboutSection.get_instance()
        about.title = "I Built This Because I Was You"
        about.content = """Fourteen years ago, I stepped off a plane with no car, limited English, and an arranged marriage that dropped me in Northern Virginia with zero network.

I started managing rentals for $300 commissions. I watched landlords get overcharged. Ignored. Misled. I watched property managers treat people's life savings like paperwork.

And I thought: "There has to be a better way."

So I built one.

Today, I manage 90 units using the same systems I use for Garden Gate clients. When I tell you "I treat your property like my own," it's not marketing. It's literally true. The toilets in my units? Same contractors who fix yours. The tenants I screen? Same process you get. The pricing I negotiate? Same hustle I use for my own portfolio.

Every dollar I save you, I'm saving myself somewhere else. Every system that works for you, I depend on for my own financial freedom.

This isn't a franchise. This isn't corporate training. This is 13 years of figuring out what actually works when your own money is on the line."""
        about.quote_text = "I don't lock clients in. I earn their trust, one transparent decision at a time."
        about.quote_author = "— Mahrukh Tariq"
        about.cta_text = "Talk to a Property Manager Today"
        about.cta_link = "#consultation"
        about.save()
        self.stdout.write(self.style.SUCCESS('✓ Seeded: About Section'))
        
        # 8. Mission/Vision Section
        mission_vision = MissionVisionSection.get_instance()
        mission_vision.mission_title = "Our Mission"
        mission_vision.mission_subtitle = "Deliver What Corporate Management Can't."
        mission_vision.mission_description = "We exist because landlords deserve better — direct access, transparent pricing, and genuine partnership. Garden Gate gives you clarity, control, and confidence in your investment."
        mission_vision.vision_title = "Our Vision"
        mission_vision.vision_subtitle = "Boutique Management That Puts Landlords First."
        mission_vision.vision_description = "We're building Northern Virginia's most trusted boutique property management firm — where landlords enjoy ownership, not endure it."
        mission_vision.cta_text = "Join Us"
        mission_vision.cta_link = "#consultation"
        mission_vision.save()
        self.stdout.write(self.style.SUCCESS('✓ Seeded: Mission/Vision Section'))
        
        # 9. Lead Magnet Section
        lead_magnet = LeadMagnetSection.get_instance()
        lead_magnet.title = "Free 15 Minute Property<br>Assessment"
        lead_magnet.subtitle = "No sales pitch. Just straight answers to:"
        lead_magnet.bullet_1 = "What your property should actually rent for"
        lead_magnet.bullet_2 = "Where you're currently losing money"
        lead_magnet.bullet_3 = "Whether we're a good fit (honest answer)"
        lead_magnet.description = "If we're not right for you, I'll tell you. If we are, you'll know exactly what happens next."
        lead_magnet.cta_text = "Find Out If We're the Right Fit"
        lead_magnet.cta_link = "#consultation"
        lead_magnet.save()
        self.stdout.write(self.style.SUCCESS('✓ Seeded: Lead Magnet Section'))
        
        # 10. Final CTA Section
        final_cta = FinalCTASection.get_instance()
        final_cta.title = "Stop Settling. Start Succeeding."
        final_cta.description = "While others chase unresponsive managers and inflated repair bills, you can work with someone who treats your property like her own."
        final_cta.cta_text = "Find Out If We're the Right Fit"
        final_cta.cta_link = "#contact"
        final_cta.save()
        self.stdout.write(self.style.SUCCESS('✓ Seeded: Final CTA Section'))
        
        self.stdout.write(self.style.SUCCESS('\n✅ Successfully seeded all content sections!'))
        self.stdout.write(self.style.WARNING('\n⚠️  Note: Credibility cards all have placeholder content. Please update them in the dashboard.'))

