import os
import random
os.environ["IMAGEMAGICK_BINARY"] = r"C:\Program Files\ImageMagick-7.1.1-Q16-HDRI\magick.exe"
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip, concatenate_videoclips
import re

# === CONFIG ===
captions_file = "captions.txt"
input_folder = "input_videos"
output_folder = "output_videos"
product_folder = "product_videos"
font_size = 60
font_color = "white"
bg_color = "transparent"  # Transparent background
font_name = r"C:\\Windows\\Fonts\\Montserrat SemiBold.ttf"

# === Product List ===
products = [
    {
        "name": "Magnetic Car Holder",
        "id": "carholder",
        "video": "carholder.mp4",
        "high_price": 10.99,
        "low_price": 10.59,  # percent
        "free_shipping": False
    },
    {
        "name": "Premium Teeth Whitening Strips",
        "id": "teethstrips",
        "video": "teethstrips.mp4",
        "high_price": 0.00,
        "low_price": 17.99,  # percent
        "free_shipping": True
    },
    {
        "name": "Citysports Threadmill",
        "id": "csports_threadmill",
        "video": "csports_threadmill.mp4",
        "high_price": 0.00,
        "low_price": 249,  # percent
        "free_shipping": True
    },
    {
        "name": "HD WirelessCarplay",
        "id": "carplay",
        "video": "carplay.mp4",
        "high_price": 0.00,
        "low_price": 55.80,  # percent
        "free_shipping": True
    }
]

# === Ensure output folder exists ===
os.makedirs(output_folder, exist_ok=True)




# === Captions Array ===
captions = [
    "My face when I saw {title} for just €{price} {shipping}.",
    "€{price} and free shipping for {title}? You've got to be kidding me.",
    "Can't believe these {title} are only €{price} {shipping}.",
    "€{price} {shipping} for {title}… I need a moment.",
    "The way I gasped seeing {title} for €{price} {shipping}.",
    "Just found {title} for €{price} {shipping} — unreal.",
    "{title} are only €{price} {shipping}... add to cart immediately.",
    "€{price} {shipping} for {title}? That's a no-brainer.",
    "Can someone explain how {title} are just €{price} {shipping}?",
    "€{price} {shipping} for {title} — that's basically a steal.",
    "I don't know who priced these {title} at €{price} {shipping}, but thank you.",
    "€{price} {shipping} for {title}? Take my money.",
    "Why are {title} only €{price} {shipping} right now?",
    "€{price} {shipping} for {title} — say less.",
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
    "€{price} {shipping} for {title} — no thoughts, just buy.",
    "The second I saw {title} were €{price} {shipping}, I blacked out and hit checkout.",
    "{title}. €{price} {shipping}. I repeat: {shipping}.",
    "No way {title} are €{price} {shipping} — someone's definitely losing their job.",
    "€{price} {shipping} for {title}? That's not a discount, that's a mistake.",
    "Whoever listed {title} at €{price} {shipping} is getting called into a meeting.",
    "{title} for €{price} {shipping}? HR's about to get a complaint.",
    "€{price} {shipping} for {title} — this has to be a pricing error.",
    "{title} at €{price} {shipping}? Heads are rolling.",
    "€{price} {shipping} for {title}… this is how people get fired.",
    "{title} are €{price} {shipping}? Someone's about to get audited.",
    "€{price} {shipping} for {title}? I hope someone triple-checked that.",
    "{title} at €{price} {shipping} — somebody hit the wrong button.",
    "No way {title} are €{price} {shipping} — that's a fireable offense.",
    "€{price} {shipping} for {title}? Somebody's packing up their desk.",
    "{title} for €{price} {shipping}? Someone's getting yelled at.",
    "€{price} {shipping} for {title} — was this approved by *anyone*?",
    "{title} at €{price} {shipping}? Someone's manager is fuming.",
    "€{price} {shipping} for {title} — that's how mistakes become viral.",
    "Who greenlit {title} for €{price} {shipping}? Y'all okay over there?",
    "€{price} {shipping} for {title} — and not one person caught that?",
    "No way {title} are €{price} {shipping} — I'm calling corporate.",
    "{title} are €{price} {shipping}? I need to speak to the pricing team.",
    "€{price} {shipping} for {title} — someone definitely messed up.",
    "€{price} {shipping} for {title}? That discount feels illegal.",
    "{title} at €{price} {shipping}? They're gonna regret this.",
    "€{price} {shipping} for {title} — someone's about to get a surprise exit interview.",
    "Who let {title} go for €{price} {shipping}? That's wild.",
    "€{price} {shipping} for {title} — someone's in *big* trouble.",
    "{title} at €{price} {shipping}? They're practically giving them away.",
    "€{price} {shipping} for {title} — someone hit \"publish\" too early.",
    "{title} are €{price} {shipping}? That's not a deal, that's sabotage.",
    "€{price} {shipping} for {title}? Someone's getting demoted today.",
    "BREAKING: {title} now just €{price} {shipping} — chaos erupts online.",
    "REPORT: {title} listed at €{price} {shipping} — shoppers in disbelief.",
    "NEWSFLASH: {title} drop to €{price} {shipping} — experts stunned.",
    "LIVE UPDATE: {title} priced at €{price} {shipping} — demand surges.",
    "HEADLINE: {title} now €{price} {shipping} — customers call it 'too good to be true.'",
    "ALERT: {title} go viral at €{price} {shipping} — sellout imminent.",
    "ECONOMY SHAKEN: {title} hit €{price} {shipping} — industry watches nervously.",
    "EXCLUSIVE: {title} available for €{price} {shipping} — limited time only.",
    "WIDESPREAD PANIC: {title} priced at €{price} {shipping} — retailers overwhelmed.",
    "MARKET DISRUPTION: {title} now €{price} {shipping} — competitors scrambling.",
    "TRENDING: {title} at €{price} {shipping} — influencers can't stop talking.",
    "ALERT ISSUED: {title} seen at €{price} {shipping} — bargain hunters rejoice.",
    "CONSUMER STUNNER: {title} drop to €{price} {shipping} — shoppers speechless.",
    "FLASH SALE REPORT: {title} listed at €{price} {shipping} — inventory flying off shelves.",
    "NEWS JUST IN: {title} now €{price} {shipping} — shoppers lose composure.",
    "WORLDWIDE REACTION: {title} hit €{price} {shipping} — social media explodes.",
    "REPORT CONFIRMED: {title} only €{price} {shipping} — 'price glitch' rumors spread.",
    "CONSUMER ALERT: {title} priced at €{price} {shipping} — buy now or regret later.",
    "FINANCIAL SHOCKWAVE: {title} drop to €{price} {shipping} — market confused.",
    "VIRAL DEAL: {title} available for €{price} {shipping} — TikTok loses it.",
    "TODAY'S HEADLINE: {title} now €{price} {shipping} — economists baffled.",
    "INSIDER SCOOP: {title} just €{price} {shipping} — stocks unaffected (somehow).",
    "MARKET WATCH: {title} go for €{price} {shipping} — everyone double-checks the site.",
    "MAJOR PRICE DROP: {title} reduced to €{price} {shipping} — the internet can't cope.",
    "CRISIS AVERTED: {title} now €{price} {shipping} — group chats rejoice.",
    "CONSUMER BUZZ: {title} selling at €{price} {shipping} — deal of the decade?",
    "PRICE DROP ALERT: {title} now €{price} {shipping} — shoppers report checkout frenzy.",
    "BREAKING ECONOMY: {title} hit €{price} {shipping} — financial Twitter reacts.",
    "GLOBAL RESPONSE: {title} priced at €{price} {shipping} — \"unreal,\" says everyone.",
    "LEAKED: {title} available at €{price} {shipping} — insiders blame intern.",
    "At €{price} {shipping}, how could I not get this {title}?",
    "This {title} is basically paying for itself at €{price} {shipping}.",
    "Me: \"I'm saving money.\" Also me: Buys the {title} for €{price} {shipping}.",
    "€{price} {shipping} for {title}? That's not a splurge, that's self-care.",
    "If the {title} is €{price} {shipping}, then yes — it's a need.",
    "€{price} {shipping}? My cart said yes before I did.",
    "This {title} at €{price} {shipping} is what financial literacy looks like.",
    "I wasn't planning to buy {title} today, but €{price} {shipping} changed that.",
    "€{price} {shipping} is basically free when it's for {title}.",
    "Who needs restraint when the {title} is €{price} {shipping}?",
    "€{price} {shipping} for this {title}? I'd be losing money *not* buying it.",
    "It's not even a purchase, it's an investment — €{price} {shipping} for {title}.",
    "When the {title} is €{price} {shipping}, you don't think — you *act.*",
    "€{price} {shipping} for {title} I'll use every day? That's called budgeting.",
    "Just a little treat: {title}, €{price} {shipping}.",
    "Tell me why this {title} being €{price} {shipping} felt like fate.",
    "You're telling me the {title} is €{price} {shipping} and I'm supposed to *walk away*?",
    "Retail therapy hits different when it's €{price} {shipping} for {title}.",
    "I'm not impulsive, I'm efficient — €{price} {shipping} for {title}.",
    "Technically, I saved money. €{price} {shipping} for {title}? Yes please.",
    "€{price} {shipping} is basically free… that's the math for this {title}.",
    "I deserve the {title}, especially if it's €{price} {shipping}.",
    "I don't make the rules — if {title} is €{price} {shipping}, I'm buying it.",
    "Some people meditate, I buy €{price} {title}s {shipping}.",
    "The {title} was €{price} {shipping}. What was I supposed to do, *not* get it?",
    "Budget-friendly *and* cute — this {title} was €{price} {shipping}.",
    "Normal people: \"I should save money.\" Me: buys {title} for €{price} {shipping}.",
    "{title} for €{price} {shipping}? That's manifestation.",
    "I call it \"smart shopping\" — €{price} {shipping} for the {title}.",
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
video_files = [
    f for f in os.listdir(input_folder)
    if f.lower().endswith((".mp4", ".mov", ".avi", ".mkv"))
]

# === User Prompts ===
while True:
    try:
        num_videos = int(input(f"How many videos do you want to create? (1-{len(video_files)}): "))
        if 1 <= num_videos <= len(video_files):
            break
        else:
            print(f"Please enter a number between 1 and {len(video_files)}.")
    except ValueError:
        print("Please enter a valid integer.")

print("\nAvailable products:")
for idx, prod in enumerate(products):
    print(f"{idx+1}. {prod['name']} (ID: {prod['id']}, High Price: ${prod['high_price']}, Low Price: {prod['low_price']}%, Free Shipping: {'Yes' if prod['free_shipping'] else 'No'})")

while True:
    try:
        prod_choice = int(input(f"Select a product (1-{len(products)}): "))
        if 1 <= prod_choice <= len(products):
            selected_product = products[prod_choice-1]
            break
        else:
            print(f"Please enter a number between 1 and {len(products)}.")
    except ValueError:
        print("Please enter a valid integer.")

# === Randomly select videos and captions ===
selected_videos = random.sample(video_files, num_videos)
selected_captions = [random.choice(captions) for _ in range(num_videos)]

# === Format captions with product details ===
formatted_captions = []
for caption_template in selected_captions:
    # Determine shipping text
    shipping_text = "with Free Shipping" if selected_product['free_shipping'] else ""
    
    # Format the caption with product details
    formatted_caption = caption_template.format(
        title=selected_product['name'],
        price=selected_product['low_price'],
        shipping=shipping_text
    )
    formatted_captions.append(formatted_caption)

# === Process each video ===
for i in range(num_videos):
    caption = formatted_captions[i]
    video_file = selected_videos[i]
    input_path = os.path.join(input_folder, video_file)

    # Sanitize caption for filename (remove/replace invalid characters)
    def sanitize_filename(s):
        s = re.sub(r'[\\/:*?"<>|]', '', s)
        s = s.strip()
        return s

    # Get file extension
    _, ext = os.path.splitext(video_file)
    MAX_FILENAME_LEN = 255 - len(ext)
    safe_caption = sanitize_filename(caption)
    truncated_caption = safe_caption[:MAX_FILENAME_LEN]
    output_filename = f"{i+1}.mp4"
    output_path = os.path.join(output_folder, output_filename)

    print(f"▶️ Processing: {video_file}")
    print(f"   ➤ Caption: \"{caption}\"")
    print(f"   ➤ Product: {selected_product['name']}")

    try:
        # --- First 3 seconds: input video with caption ---
        clip = VideoFileClip(input_path)
        # Take first 3 seconds of input video (or full video if shorter)
        input_duration = min(3, clip.duration)
        input_clip = clip.subclip(0, input_duration)
        
        txt_clip_input = TextClip(
            caption,
            fontsize=font_size,
            color=font_color,
            font=font_name,
            stroke_color="black",
            stroke_width=2,
            bg_color=bg_color,
            size=(clip.w, None),
            method='caption',
            kerning=2
        ).set_duration(input_duration)
        txt_clip_input = txt_clip_input.set_position(("center", int(clip.h * 0.22)))
        first_clip = CompositeVideoClip([input_clip, txt_clip_input])

        # --- Product video with product info overlay (full length) ---
        product_video_path = os.path.join(product_folder, selected_product['video'])
        if not os.path.exists(product_video_path):
            print(f"❌ Product video not found: {product_video_path}")
            continue

        prod_clip = VideoFileClip(product_video_path)
        print(f"   ➤ Product video duration: {prod_clip.duration:.2f}s")
        print(f"   ➤ Product video size: {prod_clip.w}x{prod_clip.h}")
        print(f"   ➤ Product video fps: {prod_clip.fps}")
        print(f"   ➤ Input video size: {clip.w}x{clip.h}")
        print(f"   ➤ Input video fps: {clip.fps}")

        # --- Ensure product video matches input video resolution and fps, and trim to 2 seconds ---
        from moviepy.video.fx.resize import resize  # Fix: import the correct resize function

        prod_clip = prod_clip.fx(resize, newsize=(clip.w, clip.h)).set_fps(clip.fps).subclip(0, min(2, prod_clip.duration)).without_audio()
        input_clip_noaudio = input_clip.without_audio()

        # --- Caption overlay for both clips ---
        txt_clip_prod = TextClip(
            caption,
            fontsize=font_size,
            color=font_color,
            font=font_name,
            stroke_color="black",
            stroke_width=2,
            bg_color=bg_color,
            size=(clip.w, None),
            method='caption',
            kerning=2
        ).set_duration(prod_clip.duration)
        txt_clip_prod = txt_clip_prod.set_position(("center", int(clip.h * 0.22)))
        product_final = CompositeVideoClip([prod_clip, txt_clip_prod])

        # --- Concatenate and write (no audio) ---
        print(f"   ➤ Concatenating {input_duration:.2f}s + {prod_clip.duration:.2f}s = {(input_duration + prod_clip.duration):.2f}s total")
        final = concatenate_videoclips([first_clip, product_final], method="compose")
        final.write_videofile(output_path, codec="libx264", audio=False, verbose=False, logger=None)

        # Clean up clips to free memory
        clip.close()
        prod_clip.close()
        final.close()
        print(f"✅ Saved to: {output_path}\n")
    except Exception as e:
        print(f"❌ Error with {video_file}: {e}\n")
