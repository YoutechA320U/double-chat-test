## double-chat-test

[gradio-gguf-chat](https://github.com/YoutechA320U/gradio-gguf-chat)で二重ロールプレイプロンプトを使って3人で会話するテスト。

モデルはEZO-gemma-2-9b系かgemma-2-27b-it、Qwen2.5などの量子化による劣化が目立たない程度のggufを使ってください。

同じプロンプトですがgemma-2よりQwen2.5の方がAI同士だけで会話してくれることが多いです。

二重ロールプレイプロンプトを使っての3人会話及びAI同士だけの会話の発生を優先しているのでロールプレイサンプルとしての安定性はやや低いです。

![Picture](https://github.com/YoutechA320U/double-chat-test/blob/master/image1.png "サンプル") 
![Picture](https://github.com/YoutechA320U/double-chat-test/blob/master/image2.png "サンプル") 

UIは基になったリポジトリと同じですがターミナルには色分けされて出力されます。

![Picture](https://github.com/YoutechA320U/double-chat-test/blob/master/image3.png "UI") 

## 履歴
    [2024/09/17] - 初回リリース
    [2024/09/22] - Qwen2.5対応。AI同士だけで会話しやすいようプロンプト変更
    [2024/10/10] - gemma-2でもAI同士だけで会話しやすいようプロンプト変更。ロールプレイ安定性を落として自由度を上げました。