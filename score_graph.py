import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np

def show_scores(old_scores, new_scores):
    names = list(old_scores.keys())
    before_scores = np.array([old_scores[name] for name in names])
    after_scores = np.array([new_scores[name] for name in names])

    # 🎨 Different color for each bar
    base_colors = ['#e6194b', '#3cb44b', '#ffe119', '#4363d8', '#f58231', '#911eb4',
                   '#42d4f4', '#f032e6', '#bfef45', '#fabed4', '#469990', '#dcbeff']
    colors = base_colors[:len(names)]

    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.bar(names, before_scores, color=colors)

    ax.set_ylim(0, max(max(before_scores), max(after_scores)) * 1.2)
    ax.set_ylabel("Score")
    ax.set_title("Scores Transition")

    num_transition_frames = 30
    pause_frames = 75  # ~2 seconds if interval=50ms
    total_frames = num_transition_frames + pause_frames

    def animate(frame):
        if frame < num_transition_frames:
            progress = frame / num_transition_frames
            current_scores = before_scores + (after_scores - before_scores) * progress
        else:
            current_scores = after_scores  # Hold final state during pause

        for bar, height in zip(bars, current_scores):
            bar.set_height(height)
        return bars

    anim = FuncAnimation(
        fig, animate,
        frames=total_frames,
        interval=50,  # ms per frame
        blit=False,
        repeat=True
    )

    # Fullscreen
    manager = plt.get_current_fig_manager()
    try:
        manager.full_screen_toggle()
    except AttributeError:
        try:
            manager.window.showMaximized()
        except:
            pass

    plt.tight_layout()
    plt.show()
