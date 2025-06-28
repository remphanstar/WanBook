"""
Gradio interface definition for WanGP.
Creates the UI components and connects them to the application's functionality.
"""
import os
import gradio as gr
import logging

logger = logging.getLogger(__name__)

def create_gradio_interface(app, config=None):
    """
    Create the Gradio interface for WanGP.
    
    Args:
        app: WanGPApp instance
        config (dict): Configuration dictionary
        
    Returns:
        gr.Blocks: Gradio interface
    """
    config = config or {}
    
    # Get available models
    model_catalog = app.model_manager.get_model_catalog()
    model_choices = [(model_info['name'], model_id) for model_id, model_info in model_catalog.items()]
    
    with gr.Blocks(title="WanGP Video Generation") as interface:
        gr.Markdown("# 🧠 WanGP - Advanced Video Generation")
        
        with gr.Tab("Text to Video"):
            with gr.Row():
                with gr.Column():
                    # Input components
                    prompt = gr.Textbox(
                        label="Prompt", 
                        placeholder="Enter a detailed description of the video you want to create",
                        lines=3
                    )
                    
                    with gr.Row():
                        model_dropdown = gr.Dropdown(
                            choices=model_choices,
                            label="Model",
                            value=model_choices[0][1] if model_choices else None
                        )
                        
                        num_frames = gr.Slider(
                            minimum=8, maximum=64, step=8, value=16,
                            label="Number of Frames"
                        )
                    
                    with gr.Row():
                        fps = gr.Slider(
                            minimum=1, maximum=30, step=1, value=8,
                            label="FPS"
                        )
                        
                        guidance_scale = gr.Slider(
                            minimum=1, maximum=20, step=0.5, value=7.5,
                            label="Guidance Scale"
                        )
                    
                    with gr.Row():
                        steps = gr.Slider(
                            minimum=10, maximum=50, step=1, value=25,
                            label="Inference Steps"
                        )
                        
                        seed = gr.Number(
                            value=-1, label="Seed (-1 for random)",
                            precision=0
                        )
                    
                    generate_button = gr.Button("Generate Video", variant="primary")
                
                with gr.Column():
                    # Output components
                    video_output = gr.Video(label="Generated Video")
                    gallery = gr.Gallery(label="Generated Frames", columns=4, rows=2, height=300)
                    
                    with gr.Accordion("Generation Info", open=False):
                        info_output = gr.JSON(label="Generation Details")
        
        with gr.Tab("Image to Video"):
            gr.Markdown("### 🖼️ Upload an image and animate it")
            
            with gr.Row():
                with gr.Column():
                    # Input components
                    input_image = gr.Image(label="Input Image", type="pil")
                    motion_prompt = gr.Textbox(
                        label="Motion Description", 
                        placeholder="Describe the motion you want to apply",
                        lines=2
                    )
                    
                    with gr.Row():
                        i2v_model_dropdown = gr.Dropdown(
                            choices=[(model_info['name'], model_id) for model_id, model_info in model_catalog.items() 
                                   if model_info.get('type') in ['i2v', 't2v']],
                            label="Model"
                        )
                        
                        i2v_frames = gr.Slider(
                            minimum=8, maximum=64, step=8, value=16,
                            label="Frames"
                        )
                    
                    i2v_generate_button = gr.Button("Animate Image", variant="primary")
                
                with gr.Column():
                    i2v_output = gr.Video(label="Generated Animation")
        
        with gr.Tab("Settings"):
            gr.Markdown("### ⚙️ Configuration Settings")
            
            with gr.Row():
                with gr.Column():
                    gr.Markdown("#### Performance Settings")
                    precision = gr.Dropdown(
                        choices=["fp32", "fp16", "int8"], 
                        value=config.get('performance', {}).get('precision', 'fp16'),
                        label="Precision"
                    )
                    
                    enable_xformers = gr.Checkbox(
                        value=config.get('performance', {}).get('enable_xformers', True),
                        label="Enable xFormers Memory Efficient Attention"
                    )
                    
                    cpu_offload = gr.Checkbox(
                        value=config.get('performance', {}).get('cpu_offload', False),
                        label="Enable CPU Offload (for low VRAM)"
                    )
                
                with gr.Column():
                    gr.Markdown("#### Output Settings")
                    output_format = gr.Dropdown(
                        choices=["mp4", "gif", "webm"], 
                        value="mp4",
                        label="Video Format"
                    )
                    
                    output_quality = gr.Slider(
                        minimum=1, maximum=10, step=1, value=8,
                        label="Output Quality"
                    )
            
            save_settings_button = gr.Button("Save Settings")
        
        # GPU Info
        gpu_info = app.gpu_manager.get_detailed_info()
        if gpu_info['cuda_available']:
            gpu_text = f"GPU: {gpu_info['device_name']} | VRAM: {gpu_info['vram_free_gb']:.2f}GB free of {gpu_info['vram_total_gb']:.2f}GB"
        else:
            gpu_text = "No GPU detected. Running in CPU mode (very slow)"
        
        gr.Markdown(f"### System Info: {gpu_text}")
        
        # Define event handlers
        def generate_video_handler(prompt, model_id, num_frames, fps, guidance_scale, steps, seed):
            try:
                output_path = app.generate_video(
                    prompt=prompt,
                    model_id=model_id,
                    num_frames=num_frames,
                    fps=fps,
                    guidance_scale=guidance_scale,
                    num_inference_steps=steps,
                    seed=seed if seed >= 0 else None
                )
                
                # TODO: This is a placeholder. In a real implementation:
                # 1. Extract frames from the video for the gallery
                # 2. Return the video path and frames
                # 3. Return generation info
                
                info = {
                    "prompt": prompt,
                    "model": model_id,
                    "frames": num_frames,
                    "fps": fps,
                    "steps": steps,
                    "seed": seed if seed >= 0 else "random",
                    "output_path": output_path
                }
                
                # Placeholder for frame extraction
                frames = []
                
                return output_path, frames, info
                
            except Exception as e:
                logger.error(f"Error in video generation: {e}")
                gr.Warning(f"Generation failed: {str(e)}")
                return None, None, {"error": str(e)}
        
        # Connect events to handlers
        generate_button.click(
            fn=generate_video_handler,
            inputs=[prompt, model_dropdown, num_frames, fps, guidance_scale, steps, seed],
            outputs=[video_output, gallery, info_output]
        )
        
        # For now, the I2V tab is a placeholder
        i2v_generate_button.click(
            fn=lambda: gr.Info("Image to Video is not implemented yet"),
            inputs=[],
            outputs=[]
        )
        
    return interface