import random


def bulb_speech(text: str) -> str:
	punctuation = [',,,', '..', ',.', ' .', ' ,', '', '', ' ..']
	emoticons = [':)', '(⁠ﾉ⁠◕⁠ヮ⁠◕⁠)⁠ﾉ⁠*⁠.⁠✧', '(⁠｡⁠•̀⁠ᴗ⁠-⁠)⁠✧', '(⁠ ⁠◜⁠‿⁠◝⁠ ⁠)', '(⁠｡⁠･⁠ω⁠･⁠｡⁠)', '(⁠⁠˘⁠︶⁠˘⁠⁠)', '(⁠﹒︠⁠ᴗ⁠﹒︡⁠)', '୧⁠(⁠﹒︠⁠ᴗ⁠﹒︡⁠)⁠୨', '( ͡⁠°⁠ ͜⁠ʖ⁠ ͡⁠°⁠)', '♪⁠～⁠(⁠´⁠ε⁠｀⁠ ⁠)', '(⁠•⁠ ⁠▽⁠ ⁠•⁠;⁠)', '(⁠˘⁠･⁠_⁠･⁠˘⁠)']

	if random.randint(0, 1) == 0:
		emoticon = ''
		if random.randint(0, 1) == 1:
			emoticon = random.choice(emoticons) 
		return f'{text.lower()}{random.choice(punctuation)} {emoticon}'
	else:
		return f'{text.capitalize()}'