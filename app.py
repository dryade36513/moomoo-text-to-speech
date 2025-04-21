import gradio as gr
import edge_tts
import asyncio
import tempfile
import os


async def get_voices():
    voices = await edge_tts.list_voices()
    return {
        f"{v['ShortName']} - {v['Locale']} ({v['Gender']})": v["ShortName"]
        for v in voices
    }


async def text_to_speech(text, voice, rate, pitch):
    if not text.strip():
        return None, "請輸入想要轉錄出來的文字。"
    if not voice:
        return None, "請選擇一種聲線(要Mutilanguage才支援中文)。"
    voice_short_name = voice.split(" - ")[0]
    rate_str = f"{rate:+d}%"
    pitch_str = f"{pitch:+d}Hz"
    communicate = edge_tts.Communicate(
        text, voice_short_name, rate=rate_str, pitch=pitch_str
    )
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
        tmp_path = tmp_file.name
        await communicate.save(tmp_path)
    return tmp_path, None


async def create_demo():
    voices = await get_voices()

    description = """
    哞哞微軟Edge TTS文字轉語音神秘機。
    調整語音速率和音調：0 為預設值，正值增加，負值減少。
    **注意：** Edge TTS 是一個雲端服務，記得連上網路。"""
    
    with gr.Blocks() as demo:
        gr.Markdown("# 哞哞微軟Edge TTS文字轉語音神秘機")
        gr.Markdown(description)
        
        with gr.Row():
            with gr.Column():
                text_input = gr.Textbox(
                    label="輸入文字", 
                    lines=5, 
                    value="幹!衝三小啦！你是北七逆!"
                )
                voice_input = gr.Dropdown(
                    choices=[""] + list(voices.keys()),
                    label="選擇語音",
                    value=list(voices.keys())[0] if voices else "",
                )
                rate_input = gr.Slider(
                    minimum=-50,
                    maximum=50,
                    value=0,
                    label="語音速率調整 (%)",
                    step=1,
                )
                pitch_input = gr.Slider(
                    minimum=-20, 
                    maximum=20, 
                    value=0, 
                    label="音調調整 (Hz)", 
                    step=1
                )
                submit_btn = gr.Button("生成語音")
                
            with gr.Column():
                audio_output = gr.Audio(
                    label="生成的音訊",
                    type="filepath",
                    autoplay=True,
                    show_download_button=True
                )
                warning_output = gr.Markdown(label="警告", visible=False)
        
        # 修正後的事件處理
        submit_btn.click(
            fn=text_to_speech,
            inputs=[text_input, voice_input, rate_input, pitch_input],
            outputs=[audio_output, warning_output]
        )
        
        gr.Markdown("免費使用Edge TTS 強大的文字轉語音功能！")
        gr.Markdown("貼心提醒:選擇聲線zh-TW、zh-CN開頭就是中文可以直接用，若是其他語言聲線則需要帶有Multilingual這個單字才支援朗讀中文!")
    
    return demo


async def main():
    demo = await create_demo()
    demo.queue(default_concurrency_limit=50)
    demo.launch(show_api=True, show_error=True)


if __name__ == "__main__":
    asyncio.run(main())
