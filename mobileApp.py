import os
os.environ["IMAGEMAGICK_BINARY"] = r"C:\Program Files\ImageMagick-7.1.1-Q16-HDRI\magick.exe"
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
import re

# === CONFIG ===
input_folder = "ugcVids"
output_folder = "mobileApp_Output"
product_folder = "mobileApp_Products"
font_size = 52
font_color = "white"
bg_color = "transparent"  # Transparent background
font_name = "Calibri-Bold"

# === Ensure output folder exists ===
os.makedirs(output_folder, exist_ok=True)

# === Captions Array ===
captions = [
    "My face when I saw {title} for just €{price} {shipping}.",
    "€{price} and free shipping for {title}? You've got to be kidding me.",
    "Can't believe these {title} are only €{price} {shipping}.",
    "€{price} {shipping} for {title}… I need a moment.",
    "The way I gasped seeing {title} for €{price} {shipping}.",
    "Just found {title} for €{price} {shipping}. unreal.",
    "{title} are only €{price} {shipping}... adding to cart immediately.",
    "€{price} {shipping} for {title}? That's a no-brainer.",
    "Can someone explain how {title} are just €{price} {shipping}?",
    "€{price} {shipping} for {title}. that's basically a steal.",
    "I don't know who priced these {title} at €{price} {shipping}, but thank you.",
    "€{price} {shipping} for {title}? Take my money.",
    "Why are {title} only €{price} {shipping} right now?",
    "€{price} {shipping} for {title}. say less.",
    "{title} for €{price} {shipping} just made my whole week.",
    "When you see {title} going for €{price} {shipping}… you don't hesitate.",
    "€{price} {shipping} for {title}? That's basically giving them away.",
    "Just grabbed {title} for €{price} {shipping} and I have no regrets.",
    "I wasn't planning on buying anything today but {title} are €{price} {shipping}.",
    "€{price} {shipping} for {title} is borderline criminal.",
    "Whoever put {title} at €{price} {shipping} deserves a raise.",
    "Me pretending to be shocked that {title} are €{price} {shipping}.",
    "I didn't need {title} but they're €{price} {shipping} sooo…",
    "Just saw {title} for €{price} {shipping} and forgot how to act.",
    "{title} are €{price} {shipping}? Okay but why does that feel illegal.",
    "Can we talk about how {title} are only €{price} {shipping} right now?",
    "How are {title} going for €{price} {shipping}?",
    "€{price} {shipping} for {title}. no thoughts, just buy.",
    "The second I saw {title} were €{price} {shipping}, I blacked out and hit checkout.",
    "{title}. €{price} {shipping}. I repeat: {shipping}.",
    "No way {title} are €{price} {shipping}. someone's definitely losing their job.",
    "€{price} {shipping} for {title}? That's not a discount, that's a mistake.",
    "Whoever listed {title} at €{price} {shipping} is getting called into a meeting.",
    "{title} for €{price} {shipping}? HR's about to get a complaint.",
    "€{price} {shipping} for {title}. this has to be a pricing error.",
    "{title} at €{price} {shipping}? Heads are rolling.",
    "€{price} {shipping} for {title}… this is how people get fired.",
    "{title} are €{price} {shipping}? Someone's about to get audited.",
    "€{price} {shipping} for {title}? I hope someone triple-checked that.",
    "{title} at €{price} {shipping}. somebody hit the wrong button.",
    "No way {title} are €{price} {shipping}. that's a fireable offense.",
    "€{price} {shipping} for {title}? Somebody's packing up their desk.",
    "{title} for €{price} {shipping}? Someone's getting yelled at.",
    "€{price} {shipping} for {title}. was this approved by *anyone*?",
    "{title} at €{price} {shipping}? Someone's manager is fuming.",
    "€{price} {shipping} for {title}. that's how mistakes become viral.",
    "Who greenlit {title} for €{price} {shipping}? Y'all okay over there?",
    "€{price} {shipping} for {title}. and not one person caught that?",
    "No way {title} are €{price} {shipping}. I'm calling corporate.",
    "{title} are €{price} {shipping}? I need to speak to the pricing team.",
    "€{price} {shipping} for {title}. someone definitely messed up.",
    "€{price} {shipping} for {title}? That discount feels illegal.",
    "{title} at €{price} {shipping}? They're gonna regret this.",
    "€{price} {shipping} for {title}. someone's about to get a surprise exit interview.",
    "Who let {title} go for €{price} {shipping}? That's wild.",
    "€{price} {shipping} for {title}. someone's in *big* trouble.",
    "{title} at €{price} {shipping}? They're practically giving them away.",
    "€{price} {shipping} for {title}. someone hit publish too early.",
    "{title} are €{price} {shipping}? That's not a deal, that's sabotage.",
    "€{price} {shipping} for {title}? Someone's getting demoted today.",
    "BREAKING: {title} now just €{price} {shipping}. chaos erupts online.",
    "REPORT: {title} listed at €{price} {shipping}. shoppers in disbelief.",
    "NEWSFLASH: {title} drop to €{price} {shipping}. experts stunned.",
    "LIVE UPDATE: {title} priced at €{price} {shipping}. demand surges.",
    "HEADLINE: {title} now €{price} {shipping}. customers call it 'too good to be true.'",
    "ALERT: {title} go viral at €{price} {shipping}. sellout imminent.",
    "ECONOMY SHAKEN: {title} hit €{price} {shipping}. industry watches nervously.",
    "EXCLUSIVE: {title} available for €{price} {shipping}. limited time only.",
    "WIDESPREAD PANIC: {title} priced at €{price} {shipping}. retailers overwhelmed.",
    "MARKET DISRUPTION: {title} now €{price} {shipping}. competitors scrambling.",
    "TRENDING: {title} at €{price} {shipping}. influencers can't stop talking.",
    "ALERT ISSUED: {title} seen at €{price} {shipping}. bargain hunters rejoice.",
    "CONSUMER STUNNER: {title} drop to €{price} {shipping}. shoppers speechless.",
    "FLASH SALE REPORT: {title} listed at €{price} {shipping}. inventory flying off shelves.",
    "NEWS JUST IN: {title} now €{price} {shipping}. shoppers lose composure.",
    "WORLDWIDE REACTION: {title} hit €{price} {shipping}. social media explodes.",
    "REPORT CONFIRMED: {title} only €{price} {shipping}. 'price glitch' rumors spread.",
    "CONSUMER ALERT: {title} priced at €{price} {shipping}. buy now or regret later.",
    "FINANCIAL SHOCKWAVE: {title} drop to €{price} {shipping}. market confused.",
    "VIRAL DEAL: {title} available for €{price} {shipping}. TikTok loses it.",
    "TODAY'S HEADLINE: {title} now €{price} {shipping}. economists baffled.",
    "INSIDER SCOOP: {title} just €{price} {shipping}. stocks unaffected (somehow).",
    "MARKET WATCH: {title} go for €{price} {shipping}. everyone double-checks the site.",
    "MAJOR PRICE DROP: {title} reduced to €{price} {shipping}. the internet can't cope.",
    "CRISIS AVERTED: {title} now €{price} {shipping}. group chats rejoice.",
    "CONSUMER BUZZ: {title} selling at €{price} {shipping}. deal of the decade?",
    "PRICE DROP ALERT: {title} now €{price} {shipping}. shoppers report checkout frenzy.",
    "BREAKING ECONOMY: {title} hit €{price} {shipping}. financial Twitter reacts.",
    "GLOBAL RESPONSE: {title} priced at €{price} {shipping}. unreal, says everyone.",
    "LEAKED: {title} available at €{price} {shipping}. insiders blame intern.",
    "At €{price} {shipping}, how could I not get this {title}?",
    "This {title} is basically paying for itself at €{price} {shipping}.",
    "Me: I'm saving money. Also me: Buys the {title} for €{price} {shipping}.",
    "€{price} {shipping} for {title}? That's not a splurge, that's self-care.",
    "If the {title} is €{price} {shipping}, then yes. it's a need.",
    "€{price} {shipping}? My cart said yes before I did.",
    "This {title} at €{price} {shipping} is what financial literacy looks like.",
    "I wasn't planning to buy {title} today, but €{price} {shipping} changed that.",
    "€{price} {shipping} is basically free when it's for {title}.",
    "Who needs restraint when the {title} is €{price} {shipping}?",
    "€{price} {shipping} for this {title}? I'd be losing money *not* buying it.",
    "It's not even a purchase, it's an investment. €{price} {shipping} for {title}.",
    "When the {title} is €{price} {shipping}, you don't think. you *act.*",
    "€{price} {shipping} for {title} I'll use every day? That's called budgeting.",
    "Just a little treat: {title}, €{price} {shipping}.",
    "Tell me why this {title} being €{price} {shipping} felt like fate.",
    "You're telling me the {title} is €{price} {shipping} and I'm supposed to *walk away*?",
    "Retail therapy hits different when it's €{price} {shipping} for {title}.",
    "I'm not impulsive, I'm efficient. €{price} {shipping} for {title}.",
    "Technically, I saved money. €{price} {shipping} for {title}? Yes please.",
    "€{price} {shipping} is basically free… that's the math for this {title}.",
    "I deserve the {title}, especially if it's €{price} {shipping}.",
    "I don't make the rules. if {title} is €{price} {shipping}, I'm buying it.",
    "Some people meditate, I buy €{price} {title}s {shipping}.",
    "The {title} was €{price} {shipping}. What was I supposed to do, *not* get it?",
    "Budget-friendly *and* cute. this {title} was €{price} {shipping}.",
    "Normal people: I should save money. Me: buys {title} for €{price} {shipping}.",
    "{title} for €{price} {shipping}? That's manifestation.",
    "I call it smart shopping. €{price} {shipping} for the {title}.",
    "If happiness is €{price} {shipping} and shaped like {title}, then I found it.",
    "They really said {title} is €{price} {shipping} and thought I wouldn't notice?",
    "€{price} {shipping} for {title}? Okay, but who approved that?",
    "So we're just casually selling {title} for €{price} {shipping} now?",
    "Not me refreshing the page because there's no way {title} is actually €{price} {shipping}.",
    "€{price} {shipping} for {title}? Yeah, that feels suspiciously generous.",
    "€{price} {shipping} for {title}? Be serious.",
    "Whoever priced {title} at €{price} {shipping} clearly doesn't know how the internet works.",
    "€{price} {shipping} for {title}… this can't be legal.",
    "Sorry, €{price} {shipping} for {title}? What economy are *you* living in?",
    "I'm supposed to just accept that {title} is €{price} {shipping} like that's normal?",
    "€{price} {shipping} for {title}? Bold of them to assume I wouldn't buy five.",
    "€{price} {shipping} for {title}? I feel like I'm stealing.",
    "€{price} {shipping} for {title}? Who do I thank for this glitch in the matrix?",
    "€{price} {shipping} for {title}? Say less. Literally speechless.",
    "€{price} {shipping} for {title}? At this point they're just giving them away.",
    "Is it just me or is €{price} {shipping} for {title} absolutely insane?",
    "They expect me to see {title} for €{price} {shipping} and just move on with my day?",
    "€{price} {shipping} for {title}… that's not a deal, that's a trap.",
    "€{price} {shipping} for {title}? Is this reverse inflation?",
    "€{price} {shipping} for {title}? I checked twice to make sure I wasn't being pranked.",
    "€{price} {shipping} for {title}? What are we, in 2006?",
    "€{price} {shipping} for {title} is not something I was emotionally prepared for.",
    "€{price} {shipping} for {title}? Okay, now I'm suspicious.",
    "€{price} {shipping} for {title}? That's a cry for help.",
    "€{price} {shipping} for {title}? Blink twice if this was a mistake.",
    "€{price} {shipping} for {title}? I'm calling someone. Not sure who, but someone.",
    "€{price} {shipping} for {title}? Do they want us to riot?",
    "€{price} {shipping} for {title}? The math isn't mathing but I'm buying it anyway.",
    "€{price} {shipping} for {title}? Is this one of those weird social experiments?",
    "€{price} {shipping} for {title}? Cool. So now I own it. Obviously."
]

# === Get list of videos, sorted ===
video_files = sorted([
    f for f in os.listdir(input_folder)
    if f.lower().endswith((".mp4", ".mov", ".avi", ".mkv"))
])

# === Process each video ===
for i, video_file in enumerate(video_files):
    # Use a simple caption for mobile app (no product placeholders)
    caption = captions[i % len(captions)]  # Cycle through captions
    
    input_path = os.path.join(input_folder, video_file)

    # Sanitize caption for filename (remove/replace invalid characters)
    def sanitize_filename(s):
        # Remove invalid characters for Windows filenames
        s = re.sub(r'[\\/:*?"<>|]', '', s)
        s = s.strip()
        return s

    # Get file extension
    _, ext = os.path.splitext(video_file)
    # Windows max filename length is 255, but need to leave room for extension
    MAX_FILENAME_LEN = 255 - len(ext)
    safe_caption = sanitize_filename(caption)
    truncated_caption = safe_caption[:MAX_FILENAME_LEN]
    output_filename = f"{truncated_caption}{ext}"
    output_path = os.path.join(output_folder, output_filename)

    print(f"▶️ Processing: {video_file}")
    print(f"   ➤ Caption: \"{caption}\"")

    try:
        clip = VideoFileClip(input_path)

        txt_clip = TextClip(
            caption,
            fontsize=font_size,
            color=font_color,
            font=font_name,
            stroke_color="black",
            stroke_width=2,
            bg_color=bg_color,
            size=(clip.w * 0.85, None),  # 85% width like ttShop.py
            method='caption',
            kerning=2
        ).set_duration(min(3, clip.duration))

        # Position: about 25% from the top (matching ttShop.py)
        txt_clip = txt_clip.set_position(("center", int(clip.h * 0.25)))

        # Cut the video to 3 seconds max
        final_clip = clip.subclip(0, min(3, clip.duration))
        final = CompositeVideoClip([final_clip, txt_clip])
        final.write_videofile(output_path, codec="libx264", audio_codec="aac", verbose=False, logger=None)

        print(f"✅ Saved to: {output_path}\n")
    except Exception as e:
        print(f"❌ Error with {video_file}: {e}\n")
