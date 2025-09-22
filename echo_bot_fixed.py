import logging
import os
import random
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from config import BOT_TOKEN

# Logging configuration
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Fixed font styles
FONT_STYLES = {
    'bold': '𝐀𝐁𝐂𝐃𝐄𝐅𝐆𝐇𝐈𝐉𝐊𝐋𝐌𝐍𝐎𝐏𝐐𝐑𝐒𝐓𝐔𝐕𝐖𝐗𝐘𝐙𝐚𝐛𝐜𝐝𝐞𝐟𝐠𝐡𝐢𝐣𝐤𝐥𝐦𝐧𝐨𝐩𝐪𝐫𝐬𝐭𝐮𝐯𝐰𝐱𝐲𝐳𝟎𝟏𝟐𝟑𝟒𝟓𝟔𝟕𝟖𝟗',
    'italic': '𝐴𝐵𝐶𝐷𝐸𝐹𝐺𝐻𝐼𝐽𝐾𝐿𝑀𝑁𝑂𝑃𝑄𝑅𝑆𝑇𝑈𝑉𝑊𝑋𝑌𝑍𝑎𝑏𝑐𝑑𝑒𝑓𝑔ℎ𝑖𝑗𝑘𝑙𝑚𝑛𝑜𝑝𝑞𝑟𝑠𝑡𝑢𝑣𝑤𝑥𝑦𝑧0123456789',
    'monospace': '𝙰𝙱𝙲𝙳𝙴𝙵𝙶𝙷𝙸𝙹𝙺𝙻𝙼𝙽𝙾𝙿𝚀𝚁𝚂𝚃𝚄𝚅𝚆𝚇𝚈𝚉𝚊𝚋𝚌𝚍𝚎𝚏𝚐𝚑𝚒𝚓𝚔𝚕𝚖𝚗𝚘𝚙𝚚𝚛𝚜𝚝𝚞𝚟𝚠𝚡𝚢𝚣𝟶𝟷𝟸𝟹𝟺𝟻𝟼𝟽𝟾𝟿',
    'script': '𝒜ℬ𝒞𝒟ℰℱ𝒢ℋℐ𝒥𝒦ℒℳ𝒩𝒪𝒫𝒬ℛ𝒮𝒯𝒰𝒱𝒲𝒳𝒴𝒵𝒶𝒷𝒸𝒹ℯ𝒻ℊ𝒽𝒾𝒿𝓀𝓁𝓂𝓃ℴ𝓅𝓆𝓇𝓈𝓉𝓊𝓋𝓌𝓍𝓎𝓏𝟢𝟣𝟤𝟥𝟦𝟧𝟨𝟩𝟪𝟫',
    'fraktur': '𝔄𝔅ℭ𝔇𝔈𝔉𝔊ℌℑ𝔍𝔎𝔏𝔐𝔑𝔒𝔓𝔔ℜ𝔖𝔗𝔘𝔙𝔚𝔛𝔜ℨ𝔞𝔟𝔠𝔡𝔢𝔣𝔤𝔥𝔦𝔧𝔨𝔩𝔪𝔫𝔬𝔭𝔮𝔯𝔰𝔱𝔲𝔳𝔴𝔵𝔶𝔷𝟘𝟙𝟚𝟛𝟜𝟝𝟞𝟟𝟠𝟡',
    'double': '𝔸𝔹ℂ𝔻𝔼𝔽𝔾ℍ𝕀𝕁𝕂𝕃𝕄ℕ𝕆ℙℚℝ𝕊𝕋𝕌𝕍𝕎𝕏𝕐ℤ𝕒𝕓𝕔𝕕𝕖𝕗𝕘𝕙𝕚𝕛𝕜𝕝𝕞𝕟𝕠𝕡𝕢𝕣𝕤𝕥𝕦𝕧𝕨𝕩𝕪𝕫𝟘𝟙𝟚𝟛𝟜𝟝𝟞𝟟𝟠𝟡',
    'circled': 'ⒶⒷⒸⒹⒺⒻⒼⒽⒾⒿⓀⓁⓂⓃⓄⓅⓆⓇⓈⓉⓊⓋⓌⓍⓎⓏⓐⓑⓒⓓⓔⓕⓖⓗⓘⓙⓚⓛⓜⓝⓞⓟⓠⓡⓢⓣⓤⓥⓦⓧⓨⓩ⓪①②③④⑤⑥⑦⑧⑨',
    'squared': '🄰🄱🄲🄳🄴🄵🄶🄷🄸🄹🄺🄻🄼🄽🄾🄿🅀🅁🅂🅃🅄🅅🅆🅇🅈🅉🅐🅑🅒🅓🅔🅕🅖🅗🅘🅙🅚🅛🅜🅝🅞🅟🅠🅡🅢🅣🅤🅥🅦🅧🅨🅩🄌①②③④⑤⑥⑦⑧⑨',
    'smallcaps': 'ABCDEFGHIJKLMNOPQRSTUVWXYZᴀʙᴄᴅᴇғɢʜɪᴊᴋʟᴍɴᴏᴘǫʀsᴛᴜᴠᴡxʏᴢ0123456789',
    'tiny': 'ABCDEFGHIJKLMNOPQRSTUVWXYZᵃᵇᶜᵈᵉᶠᵍʰᶦʲᵏˡᵐⁿᵒᵖqʳˢᵗᵘᵛʷˣʸᶻ⁰¹²³⁴⁵⁶⁷⁸⁹',
    'upside_down': '∀qƆpƎℲפHIſʞ˥WNOԀὉᴚS⊥∩ΛMXʎZɐqɔpǝɟƃɥᴉɾʞʅɯuodbɹsʇnʌʍxʎz0⇂ᄅƐㄣϛ9ㄥ86',
    'strikethrough': 'A̶B̶C̶D̶E̶F̶G̶H̶I̶J̶K̶L̶M̶N̶O̶P̶Q̶R̶S̶T̶U̶V̶W̶X̶Y̶Z̶a̶b̶c̶d̶e̶f̶g̶h̶i̶j̶k̶l̶m̶n̶o̶p̶q̶r̶s̶t̶u̶v̶w̶x̶y̶z̶0̶1̶2̶3̶4̶5̶6̶7̶8̶9̶',
    'underline': 'A̲B̲C̲D̲E̲F̲G̲H̲I̲J̲K̲L̲M̲N̲O̲P̲Q̲R̲S̲T̲U̲V̲W̲X̲Y̲Z̲a̲b̲c̲d̲e̲f̲g̲h̲i̲j̲k̲l̲m̲n̲o̲p̲q̲r̲s̲t̲u̲v̲w̲x̲y̲z̲0̲1̲2̲3̲4̲5̲6̲7̲8̲9̲',
    'double_underline': 'A̳B̳C̳D̳E̳F̳G̳H̳I̳J̳K̳L̳M̳N̳O̳P̳Q̳R̳S̳T̳U̳V̳W̳X̳Y̳Z̳a̳b̳c̳d̳e̳f̳g̳h̳i̳j̳k̳l̳m̳n̳o̳p̳q̳r̳s̳t̳u̳v̳w̳x̳y̳z̳0̳1̳2̳3̳4̳5̳6̳7̳8̳9̳',
    'overline': 'A̅B̅C̅D̅E̅F̅G̅H̅I̅J̅K̅L̅M̅N̅O̅P̅Q̅R̅S̅T̅U̅V̅W̅X̅Y̅Z̅a̅b̅c̅d̅e̅f̅g̅h̅i̅j̅k̅l̅m̅n̅o̅p̅q̅r̅s̅t̅u̅v̅w̅x̅y̅z̅0̅1̅2̅3̅4̅5̅6̅7̅8̅9̅',
    'dot_above': 'ȦḂĊḊĖḞĠḢİJ̇K̇L̇ṀṄȮṖQ̇ṘṠṪU̇V̇ẆẊẎŻȧḃċḋėḟġḣi̇j̇k̇l̇ṁṅȯṗq̇ṙṡṫu̇v̇ẇẋẏż0̇1̇2̇3̇4̇5̇6̇7̇8̇9̇',
    'dot_below': 'ẠḄC̣ḌẸF̣G̣ḤỊJ̣ḲḶṂṆỌP̣Q̣ṚṢṬỤṾẈX̣ỴẒạḅc̣ḍẹf̣g̣ḥịj̣ḳḷṃṇọp̣q̣ṛṣṭụṿẉx̣ỵẓ0̣1̣2̣3̣4̣5̣6̣7̣8̣9̣',
    'tilde': 'ÃB̃C̃D̃ẼF̃G̃H̃ĨJ̃K̃L̃M̃ÑÕP̃Q̃R̃S̃T̃ŨṼW̃X̃ỸZ̃ãb̃c̃d̃ẽf̃g̃h̃ĩj̃k̃l̃m̃ñõp̃q̃r̃s̃t̃ũṽw̃x̃ỹz̃0̃1̃2̃3̃4̃5̃6̃7̃8̃9̃',
    'acute': 'ÁB́ĆD́ÉF́ǴH́ÍJ́ḰĹḾŃÓṔQ́ŔŚT́ÚV́ẂX́ÝŹáb́ćd́éf́ǵh́íj́ḱĺḿńóṕq́ŕśt́úv́ẃx́ýź0́1́2́3́4́5́6́7́8́9́',
    'grave': 'ÀB̀C̀D̀ÈF̀G̀H̀ÌJ̀K̀L̀M̀ǸÒP̀Q̀R̀S̀T̀ÙV̀ẀX̀ỲZ̀àb̀c̀d̀èf̀g̀h̀ìj̀k̀l̀m̀ǹòp̀q̀r̀s̀t̀ùv̀ẁx̀ỳz̀0̀1̀2̀3̀4̀5̀6̀7̀8̀9̀',
    'circumflex': 'ÂB̂ĈD̂ÊF̂ĜĤÎĴK̂L̂M̂N̂ÔP̂Q̂R̂ŜT̂ÛV̂ŴX̂ŶẐâb̂ĉd̂êf̂ĝĥîĵk̂l̂m̂n̂ôp̂q̂r̂ŝt̂ûv̂ŵx̂ŷẑ0̂1̂2̂3̂4̂5̂6̂7̂8̂9̂',
    'caron': 'ǍB̌ČĎĚF̌ǦȞÍJ̌ǨĽM̌ŇÓP̌Q̌ŘŠŤÚV̌W̌X̌ÝŽǎb̌čďěf̌ǧȟíǰǩľm̌ňóp̌q̌řšťúv̌w̌x̌ýž0̌1̌2̌3̌4̌5̌6̌7̌8̌9̌',
    'breve': 'ĂB̆C̆D̆ĔF̆ĞH̆ĬJ̆K̆L̆M̆N̆ŎP̆Q̆R̆S̆T̆ŬV̆W̆X̆ŶZ̆ăb̆c̆d̆ĕf̆ğh̆ĭj̆k̆l̆m̆n̆ŏp̆q̆r̆s̆t̆ŭv̆w̆x̆ŷz̆0̆1̆2̆3̆4̆5̆6̆7̆8̆9̆',
    'ring': 'ÅB̊C̊D̊E̊F̊G̊H̊I̊J̊K̊L̊M̊N̊O̊P̊Q̊R̊S̊T̊ŮV̊W̊X̊Y̊Z̊åb̊c̊d̊e̊f̊g̊h̊i̊j̊k̊l̊m̊n̊o̊p̊q̊r̊s̊t̊ův̊ẘx̊ẙz̊0̊1̊2̊3̊4̊5̊6̊7̊8̊9̊',
    'macron': 'ĀB̄C̄D̄ĒF̄ḠH̄ĪJ̄K̄L̄M̄N̄ŌP̄Q̄R̄S̄T̄ŪV̄W̄X̄ȲZ̄āb̄c̄d̄ēf̄ḡh̄īj̄k̄l̄m̄n̄ōp̄q̄r̄s̄t̄ūv̄w̄x̄ȳz̄0̄1̄2̄3̄4̄5̄6̄7̄8̄9̄',
    'cedilla': 'A̧B̧ÇḐȨF̧ĢḨI̧J̧ĶĻM̧ŅO̧P̧Q̧ŖŞŢU̧V̧W̧X̧Y̧Z̧a̧b̧çḑȩf̧ģḩi̧j̧ķļm̧ņo̧p̧q̧ŗşţu̧v̧w̧x̧y̧z̧0̧1̧2̧3̧4̧5̧6̧7̧8̧9̧',
    'ogonek': 'ĄB̨C̨D̨ĘF̨G̨H̨ĮJ̨K̨L̨M̨N̨ǪP̨Q̨R̨S̨T̨ŲV̨W̨X̨Y̨Z̨ąb̨c̨d̨ęf̨g̨h̨įj̨k̨l̨m̨n̨ǫp̨q̨r̨s̨t̨ųv̨w̨x̨y̨z̨0̨1̨2̨3̨4̨5̨6̨7̨8̨9̨',
    'hook_above': 'ẢB̉C̉D̉ẺF̉G̉H̉ỈJ̉K̉L̉M̉N̉ỎP̉Q̉R̉S̉T̉ỦV̉W̉X̉ỶZ̉ảb̉c̉d̉ẻf̉g̉h̉ỉj̉k̉l̉m̉n̉ỏp̉q̉r̉s̉t̉ủv̉w̉x̉ỷz̉0̉1̉2̉3̉4̉5̉6̉7̉8̉9̉',
    'horn': 'ẢB̛C̛D̛ẺF̛G̛H̛ỈJ̛K̛L̛M̛N̛ỎP̛Q̛R̛S̛T̛ỦV̛W̛X̛ỶZ̛ảb̛c̛d̛ẻf̛g̛h̛ỉj̛k̛l̛m̛n̛ỏp̛q̛r̛s̛t̛ủv̛w̛x̛ỷz̛0̛1̛2̛3̛4̛5̛6̛7̛8̛9̛',
    'stroke': 'ȺB̸C̸D̸E̸F̸G̸H̸I̸J̸K̸L̸M̸N̸O̸P̸Q̸R̸S̸T̸U̸V̸W̸X̸Y̸Z̸Ⱥb̸c̸d̸e̸f̸g̸h̸i̸j̸k̸l̸m̸n̸o̸p̸q̸r̸s̸t̸u̸v̸w̸x̸y̸z̸0̸1̸2̸3̸4̸5̸6̸7̸8̸9̸',
}

# Normal characters for replacement
NORMAL_CHARS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'

def style_text(text: str, style: str = None) -> str:
    """Converts text to the selected font style"""
    if style is None:
        style = random.choice(list(FONT_STYLES.keys()))
    
    if style not in FONT_STYLES:
        return text
    
    styled_text = ""
    for char in text:
        if char in NORMAL_CHARS:
            index = NORMAL_CHARS.index(char)
            styled_text += FONT_STYLES[style][index]
        else:
            styled_text += char
    
    return styled_text

def get_fancy_response(text: str) -> str:
    """Generates a beautiful response with different styles"""
    responses = [
        f"✨ {style_text(text, 'bold')} ✨",
        f"🌟 {style_text(text, 'script')} 🌟",
        f"💫 {style_text(text, 'double')} 💫",
        f"⭐ {style_text(text, 'circled')} ⭐",
        f"🔮 {style_text(text, 'fraktur')} 🔮",
        f"✨ {style_text(text, 'monospace')} ✨",
        f"🌟 {style_text(text, 'italic')} 🌟",
        f"💎 {style_text(text, 'squared')} 💎",
        f"🔥 {style_text(text, 'smallcaps')} 🔥",
        f"⚡ {style_text(text, 'tiny')} ⚡",
        f"🌀 {style_text(text, 'upside_down')} 🌀",
        f"❌ {style_text(text, 'strikethrough')} ❌",
        f"📝 {style_text(text, 'underline')} 📝",
        f"📋 {style_text(text, 'double_underline')} 📋",
        f"📏 {style_text(text, 'overline')} 📏",
        f"🔸 {style_text(text, 'dot_above')} 🔸",
        f"🔹 {style_text(text, 'dot_below')} 🔹",
        f"🌊 {style_text(text, 'tilde')} 🌊",
        f"⚡ {style_text(text, 'acute')} ⚡",
        f"⚡ {style_text(text, 'grave')} ⚡",
        f"⚡ {style_text(text, 'circumflex')} ⚡",
        f"⚡ {style_text(text, 'caron')} ⚡",
        f"⚡ {style_text(text, 'breve')} ⚡",
        f"⚡ {style_text(text, 'ring')} ⚡",
        f"⚡ {style_text(text, 'macron')} ⚡",
        f"⚡ {style_text(text, 'cedilla')} ⚡",
        f"⚡ {style_text(text, 'ogonek')} ⚡",
        f"⚡ {style_text(text, 'hook_above')} ⚡",
        f"⚡ {style_text(text, 'horn')} ⚡",
        f"⚡ {style_text(text, 'stroke')} ⚡"
    ]
    
    return random.choice(responses)

def get_all_styles_response(text: str) -> str:
    """Generates a response with all styles at once"""
    response = "🎨 ALL FONT STYLES 🎨\n\n"
    
    styles_info = [
        ("𝐁𝐨𝐥𝐝", "bold", "✨"),
        ("𝐴𝐵𝐶", "italic", "🌟"),
        ("𝒮𝒸𝓇𝒾𝓅𝓉", "script", "💫"),
        ("ⒸⒾⓇⒸⓁⒺⒹ", "circled", "⭐"),
        ("𝔉𝔯𝔞𝔨𝔱𝔲𝔯", "fraktur", "🔮"),
        ("𝕠𝕠", "double", "💎"),
        ("𝚘", "monospace", "✨"),
        ("", "squared", "🌟"),
        (" ᴀʙᴄ", "smallcaps", "🔥"),
        ("⚡ ᵃᵇᶜ", "tiny", "⚡"),
        (" ɐqɔ", "upside_down", "🌀"),
        ("A̶B̶C̶", "strikethrough", "❌"),
        ("A̲B̲C̲", "underline", "📝"),
        ("A̳B̳C̳", "double_underline", "📋"),
        ("A̅B̅C̅", "overline", "📏"),
        ("ȦḂĊ", "dot_above", "🔸"),
        ("ẠḄC̣", "dot_below", "🔹"),
        ("ÃB̃C̃", "tilde", "🌊"),
        ("ÁB́Ć", "acute", "⚡"),
        ("ÀB̀C̀", "grave", "⚡"),
        ("ÂB̂Ĉ", "circumflex", "⚡"),
        ("ǍB̌Č", "caron", "⚡"),
        ("ĂB̆C̆", "breve", "⚡"),
        ("ÅB̊C̊", "ring", "⚡"),
        ("ĀB̄C̄", "macron", "⚡"),
        ("A̧B̧Ç", "cedilla", "⚡"),
        ("ĄB̨C̨", "ogonek", "⚡"),
        ("ẢB̉C̉", "hook_above", "⚡"),
        ("ẢB̛C̛", "horn", "⚡"),
        ("ȺB̸C̸", "stroke", "⚡")
    ]
    
    for style_name, style_key, emoji in styles_info:
        styled_text = style_text(text, style_key)
        if style_name:
            response += f"{emoji} {style_name}: {styled_text}\n"
        else:
            response += f"{emoji} {style_key}: {styled_text}\n"
    
    response += "\n🔮 Every time will be a random style! 🔮"
    return response

def get_emoji_response(text: str) -> str:
    """Generates a response with emoticons and symbols"""
    emojis = ["✨", "🌟", "💫", "⭐", "🔮", "💎", "🎭", "🎨", "🎪", "🎯", "🎲", "🎸", "🎺", "🎻", "🎼", "🎵", "🎶"]
    symbols = ["◈", "◉", "◎", "◊", "◌", "◍", "◎", "◐", "◑", "◒", "◓", "◔", "◕", "◖", "◗", "◘", "◙"]
    
    style = random.choice(list(FONT_STYLES.keys()))
    styled_text = style_text(text, style)
    
    emoji = random.choice(emojis)
    symbol = random.choice(symbols)
    
    responses = [
        f"{emoji} {styled_text} {emoji}",
        f"{symbol} {styled_text} {symbol}",
        f"{emoji} {symbol} {styled_text} {symbol} {emoji}",
        f"┌─ {styled_text} ─┐\n└─ {emoji} ─┘",
        f"╔══ {styled_text} ══╗\n╚══ {emoji} ══╝"
    ]
    
    return random.choice(responses)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Command handler for /start"""
    user = update.effective_user
    welcome_text = f'Hello {user.first_name}! 👋\n\n'
    welcome_text += '🎨 I am an echo bot with beautiful fonts! 🎨\n\n'
    welcome_text += '✨ Send me any message and I will repeat it in different styles:\n'
    welcome_text += '• 𝐁𝐨𝐥𝐝 (bold)\n'
    welcome_text += '• 𝐴𝐵𝐶 (italic)\n'
    welcome_text += '• 𝓢𝓬𝓻𝓲𝓹𝓽 (script)\n'
    welcome_text += '• ⒸⒾⓇⒸⓁⒺⒹ (circled)\n'
    welcome_text += '• 𝔉𝔯𝔞𝔨𝔱𝔲𝔯 (fraktur)\n'
    welcome_text += '• 𝕄𝕠𝕟𝕠𝕤𝕡𝕒𝕔𝕖 (monospace)\n'
    welcome_text += '• ᴀʙᴄ (small caps)\n'
    welcome_text += '• ᵃᵇᶜ (tiny)\n'
    welcome_text += '• ɐqɔ (upside down)\n\n'
    welcome_text += '🔮 Every time will be a new style! 🔮'
    
    await update.message.reply_text(welcome_text)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Command handler for /help"""
    help_text = '🎨 Echo bot with beautiful fonts 🎨\n\n'
    help_text += '📋 Available commands:\n'
    help_text += '/start - Start working with the bot\n'
    help_text += '/help - Show this help\n\n'
    help_text += '✨ Features:\n'
    help_text += '• Repeats texts in 30+ different font styles\n'
    help_text += '• Supports photos, documents, stickers, videos\n'
    help_text += '• New response style every time\n'
    help_text += '• Beautiful emojis and symbols\n'
    help_text += '• Special styles: small caps, tiny, upside down\n\n'
    help_text += '🔮 Just send me a message! 🔮'
    
    await update.message.reply_text(help_text)

async def echo_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handler for all text messages - repeats them in styled format"""
    user_message = update.message.text
    user = update.effective_user
    
    # Log the message
    logger.info(f"User {user.first_name} ({user.id}) sent: {user_message}")
    
    # Check if this is the user's first message
    user_id = user.id
    if not hasattr(context, 'user_first_message'):
        context.user_first_message = set()
    
    # If this is the user's first message, show all styles
    if user_id not in context.user_first_message:
        context.user_first_message.add(user_id)
        styled_response = get_all_styles_response(user_message)
    else:
        # Generate styled response
        response_type = random.choice(['fancy', 'emoji', 'simple'])
        
        if response_type == 'fancy':
            styled_response = get_fancy_response(user_message)
        elif response_type == 'emoji':
            styled_response = get_emoji_response(user_message)
        else:  # simple
            style = random.choice(list(FONT_STYLES.keys()))
            styled_text = style_text(user_message, style)
            styled_response = f"✨ {styled_text} ✨"
    
    # Send styled response
    await update.message.reply_text(styled_response)

async def echo_photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Photo handler - repeats photo with caption"""
    user = update.effective_user
    caption = update.message.caption or "No caption"
    
    logger.info(f"User {user.first_name} ({user.id}) sent photo with caption: {caption}")
    
    # Repeat photo
    await update.message.reply_photo(
        photo=update.message.photo[-1].file_id,
        caption=f"🖼️ Echo photo: {caption}"
    )

async def echo_document(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Document handler - repeats document"""
    user = update.effective_user
    document = update.message.document
    
    logger.info(f"User {user.first_name} ({user.id}) sent document: {document.file_name}")
    
    # Repeat document
    await update.message.reply_document(
        document=document.file_id,
        caption=f"📄 Echo document: {document.file_name}"
    )

async def echo_sticker(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sticker handler - repeats sticker"""
    user = update.effective_user
    
    logger.info(f"User {user.first_name} ({user.id}) sent sticker")
    
    # Repeat sticker
    await update.message.reply_sticker(sticker=update.message.sticker.file_id)

async def echo_voice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Voice message handler - repeats them"""
    user = update.effective_user
    
    logger.info(f"User {user.first_name} ({user.id}) sent voice message")
    
    # Repeat voice message
    await update.message.reply_voice(voice=update.message.voice.file_id)

async def echo_video(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Video handler - repeats video"""
    user = update.effective_user
    caption = update.message.caption or "No caption"
    
    logger.info(f"User {user.first_name} ({user.id}) sent video with caption: {caption}")
    
    # Repeat video
    await update.message.reply_video(
        video=update.message.video.file_id,
        caption=f"🎥 Echo video: {caption}"
    )

def main() -> None:
    """Main function to start the bot"""
    # Create application
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Add command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    
    # Add message handlers
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo_message))
    application.add_handler(MessageHandler(filters.PHOTO, echo_photo))
    application.add_handler(MessageHandler(filters.Document.ALL, echo_document))
    application.add_handler(MessageHandler(filters.Sticker.ALL, echo_sticker))
    application.add_handler(MessageHandler(filters.VOICE, echo_voice))
    application.add_handler(MessageHandler(filters.VIDEO, echo_video))
    
    # Start the bot
    print("🤖 Bot is starting...")
    print("Press Ctrl+C to stop")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()