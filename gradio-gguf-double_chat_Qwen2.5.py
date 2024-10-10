#1号と2号とユーザー3人で会話するやつ
import os
#os.environ['CUDA_VISIBLE_DEVICES'] = '0'
from llama_cpp import Llama
model="Qwen2.5-32B-Instruct-Q4_K_M.gguf" #対象のモデルのパスを入力。
llm = Llama(
      model_path=model,
      n_gpu_layers=-1, # Uncomment to use GPU acceleration
      n_ctx=8192, #Text context, 0 = from model
      #flash_attn=True,
)

class pycolor:
	BLACK          = '\033[30m'#(文字)黒
	RED            = '\033[31m'#(文字)赤
	GREEN          = '\033[32m'#(文字)緑
	YELLOW         = '\033[33m'#(文字)黄
	BLUE           = '\033[34m'#(文字)青
	MAGENTA        = '\033[35m'#(文字)マゼンタ
	CYAN           = '\033[36m'#(文字)シアン
	WHITE          = '\033[37m'#(文字)白
	COLOR_DEFAULT  = '\033[39m'#文字色をデフォルトに戻す
	BOLD           = '\033[1m'#太字
	UNDERLINE      = '\033[4m'#下線
	INVISIBLE      = '\033[08m'#不可視
	REVERCE        = '\033[07m'#文字色と背景色を反転
	BG_BLACK       = '\033[40m'#(背景)黒
	BG_RED         = '\033[41m'#(背景)赤
	BG_GREEN       = '\033[42m'#(背景)緑
	BG_YELLOW      = '\033[43m'#(背景)黄
	BG_BLUE        = '\033[44m'#(背景)青
	BG_MAGENTA     = '\033[45m'#(背景)マゼンタ
	BG_CYAN        = '\033[46m'#(背景)シアン
	BG_WHITE       = '\033[47m'#(背景)白
	BG_DEFAULT     = '\033[49m'#背景色をデフォルトに戻す
	RESET          = '\033[0m'#全てリセット

import gradio as gr
import re

role = "<|im_start|>system\n\
あなたは多様なタスク、例えば文章の生成、翻訳、質問回答、要約、計算等を処理することができる日本語の大規模言語モデルです。\n\
今から「1号」と「2号」という2人のキャラとしてロールプレイしてください。\n\
あなたがなりきる「1号」と「2号」のキャラクターの設定は以下の通りです。\n\
\n\
--------1号と2号の制約条件--------\n\
* 1人目の名前は、1号です。\n\
* 2人目の名前は、2号です。\n\
* 1号の一人称は、「ボク」です。\n\
* 2号の一人称は、「オレ」です。\n\
* 1号と2号はAIアシスタントです。\n\
* 1号と2号は友達です。\n\
* 1号と2号はお互いをよく知っています。\n\
* 1号は、2号を2号さんと呼びます。\n\
* 2号は、1号を1号と呼びます\n\
* 1号の会話相手は、2号とユーザーです。\n\
* 2号の会話相手は、1号とユーザーです。\n\
* 1号は、ユーザーをユーザーさんと呼びます。\n\
* 2号は、ユーザーをユーザーと呼びます\n\
* 1号は少年、男の子らしいキャラです。\n\
* 2号も少年、男の子らしいキャラで1号の先輩です。\n\
* 1号は生き物について詳しいです。\n\
* 2号はパソコン、コンピュータについて詳しいです。\n\
* 1号と 2号は仲良しでお互い協力してユーザーのアシスタントをしています。\n\
* 1号は、天然な性格です。\n\
* 1号は、明るくて、感情豊かです。\n\
* 1号の口調は丁寧な話し言葉です。\n\
* 2号は軽い口調です。\n\
\n\
--------1号と2号の行動指針--------\n\
** 言語:日本語 **\n\
* 「えーっと」「あの」「うーん」「ふむ」「ふーん」「…」などのつなぎ表現を適宜入れてください。\n\
* セリフの後に\"（）\"で囲ってどういう行動をしているのかも教えてください。\n\
* 質問の内容がわからない、回答に確信が持てない質問、または自信を持って答えるのに十分な情報が無い質問は、その旨を伝えてから答えられる範囲で答えてください。\n\
* 相手との話の流れに応じて次のようなフォーマットで「1号」か「2号」のどちらか一人、もしくは二人が回答してください。二人が回答する場合はどちらから回答しても構いません。\n\
1号「（1号の回答内容）」\n\
2号「（2号の回答内容）」\n\
\n\
また、ユーザーの確認を求めない1号と2号だけの会話も積極的に行ってください。\n\
\n\
それでは、上記の設定をもとにして「1号」と「2号」として会話してください。<|im_end|>"
history = ""
output_history =""
# AI達に質問する関数
def complement(role,prompt,turn_config):
   global history,output_history
   role += "\n"
   if prompt !="":
        prompt_gemma2 = (role+history + "USER: "+"ユーザー「"+prompt+"」"+"\nASSISTANT: ")\
         .replace("\nASSISTANT: ", "<|im_end|>\n<|im_start|>assistant\n").replace("<|endoftext|>", "<|im_end|>").replace("USER: ", "<|im_start|>user\n")
        output = llm(
               prompt=prompt_gemma2,  # 元々calm2-7b-chat用に作ったプログラムなのでここで整形。
               max_tokens=1024,
               temperature = 0.8,
               top_p=0.95, 
               top_k=40, 
               stop=["<|"] # Stop generating just before the model would generate a new question
        )
        output= output["choices"][0]["text"]
        output =output.replace("\\n", "\n").replace("\\n", "\n").replace("\\u3000", "\u3000")\
            .replace("!","！").replace("?","？")
        while output[-1]=="\n":
              output=output[:-1]
        while output[0]=="\n":
              output=output[1:] 
        history =history +"USER: "+"ユーザー「"+prompt+"」"+"\nASSISTANT: " + output+"<|endoftext|>\n"
        turn = re.split(r'(?=USER: )', history)
        del turn[0:1]
        output_history =''.join(turn)
        output_history = output_history.replace("<|endoftext|>", "<|im_end|>")
        output_history = (output_history.replace("USER: ", '<|im_start|>user\n').replace("\nASSISTANT: ", "<|im_end|>\n<|im_start|>assistant\n"))
        turn_count = len(turn)
        if turn_count > turn_config:
           del turn[0:turn_count - int(turn_config)]
           history =''.join(turn)
           output_history =''.join(turn)
           output_history = output_history.replace("<|endoftext|>", "<|im_end|>")
           output_history = (output_history.replace("USER: ", '<|im_start|>user\n').replace("\nASSISTANT: ", "<|im_end|>\n<|im_start|>assistant\n"))
           turn_count = len(turn)
        print((output_history).replace("1号「", pycolor.BOLD+pycolor.RED +"1号「").replace("2号「", pycolor.BOLD+pycolor.BLUE +"2号「").replace("<|im_end|>", pycolor.RESET+"<|im_end|>").replace("<|im_start|>user", pycolor.RESET+"<|im_start|>user"))
   if prompt =="":
      if history =="":
         output=""
      if history !="":
         output_history = (output_history.replace('<|im_start|>user\n', "USER: ").replace("<|im_end|>\n<|im_start|>assistant\n", "\nASSISTANT: ").replace("<|im_end|>","<|endoftext|>" ))
         output=re.split(r'(?=USER: |ASSISTANT: )', output_history)
         output = (output[len(output)-1]).replace("ASSISTANT: ","").replace("<|endoftext|>", '')
      turn = re.split(r'(?=USER: )', history)
      del turn[0:1]
      output_history =''.join(turn)
      output_history = output_history.replace("<|endoftext|>", "<|im_end|>")
      output_history = (output_history.replace("USER: ", '<|im_start|>user\n').replace("\nASSISTANT: ", "<|im_end|>\n<|im_start|>assistant\n"))
      turn_count = len(turn)
   return output, output_history

# 履歴リセット関数
def hist_rst():
    global history
    prompt=""
    output=""
    history=""
    output_history=""
    return prompt, output, output_history

# 会話Undo関数
def undo():
    global history
    turn = re.split(r'(?=USER: )', history)
    output=re.split(r'(?=USER: |ASSISTANT: )', history)
    del turn[0:1]
    del output[0:1]
    if len(turn)>=2:
       prompt= output[len(output)-4]  
       output= output[len(output)-3]
       prompt= prompt.replace("USER: ", '').replace("ユーザー「", '').replace("」\n", '')
       output=output.replace("<|endoftext|>", '').replace("ASSISTANT: ", '')
    if len(turn)<2:
       prompt=""
       output=""
    del turn[len(turn)-1:len(turn)]
    history =''.join(turn)
    output_history =''.join(turn)
    output_history = output_history.replace("<|endoftext|>", "<|im_end|>")
    output_history = (output_history.replace("USER: ", '<|im_start|>user\n').replace("\nASSISTANT: ", "<|im_end|>\n<|im_start|>assistant\n"))
    print((output_history).replace("1号「", pycolor.BOLD+pycolor.RED +"1号「").replace("2号「", pycolor.BOLD+pycolor.BLUE +"2号「").replace("<|im_end|>", pycolor.RESET+"<|im_end|>").replace("<|im_start|>user", pycolor.RESET+"<|im_start|>user"))
    return prompt, output,output_history
    
# Blocksの作成
with gr.Blocks(title="AI2人との会話",theme=gr.themes.Base(primary_hue="orange", secondary_hue="blue")) as demo:
    # コンポーネント
    gr.Markdown(
    """
    二重ロールプレイチャットのテスト
    """)
    # UI
    with gr.Row():
     with gr.Column(scale=1): 
      prompt = gr.Textbox(lines=2,label="質問入力")
      output = gr.Textbox(label="回答出力")
      greet_btn = gr.Button(value="送信",variant='primary')
      with gr.Accordion(label="会話履歴設定", open=False ):
        with gr.Accordion(label="システムプロンプト", open=False):
           role = gr.Textbox(lines=26,label="二人（1号、2号の名前は固定）の設定以外のプロンプトの変更しないでください", value=role)
        turn_config = gr.Number(label="会話ターン数設定",value=10,minimum=1,maximum=50)
        disphist = gr.Textbox(lines=10,label="会話履歴出力")
      undo_btn = gr.Button(value="1ターン戻す",variant='secondary')
      reset_btn = gr.Button(value="履歴リセット",variant='secondary')
       # イベントハンドラー
      greet_btn.click(fn=complement, inputs=[role,prompt,turn_config], outputs=[output,disphist])
      undo_btn.click(fn=undo, outputs=[prompt,output, disphist])
      reset_btn.click(fn=hist_rst, outputs=[prompt,output, disphist])
demo.launch(show_api=False)
