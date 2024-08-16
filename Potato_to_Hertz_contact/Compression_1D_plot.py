from manim import *
# from manim.opengl import *
#from manim_slides import Slide
# from manim_meshes import *
# from moderngl import *
import cv2
import os, sys, subprocess, time, shutil
import math
import numpy as np

# Render slides:
# manim Compression_1D_plot.py --disable_caching -pqh --fps=30
# Play slides
# manim-slides SquareToCircle --start-paused -r 1280 720
# Convert slides to HTML
# manim-slides convert SquareToCircle --open HTML_slides_v2

# Convert slides to pptx
# manim-slides convert --to=pptx SquareToCircle pptx_slides.pptx

# Configure keys for slides
# manim-slides wizard

# Render with opengl
# manim -qm -p --renderer=opengl test_manim.py SquareToCircle

# Render with setting from config files (remoe flags which overwrite properties)
# manim Compression_1D_plot.py --disable_caching -p

x_ini = 0.0001
x_cur_seq = x_ini
x_cum_seq = x_cur_seq
log_step = 0.002
y_log_scaling = 90
x_seq = [x_cum_seq]
y_seq = [math.log(x_cum_seq)**2]
while (x_cum_seq < 1.):
    log_slope = 2*math.log(x_cum_seq)/x_cum_seq/y_log_scaling
    x_cur_seq = (log_step**2/(1+log_slope**2))**0.5
    x_cum_seq = x_cum_seq + x_cur_seq
    x_seq.append(x_cum_seq)
    y_seq.append(math.log(x_cum_seq)**2/y_log_scaling)
# Some smooth function for the time step to make smooth animation of bar compression
#t_seq = [(0.5-np.cos(i/len(x_seq)*math.pi)*0.5) for i in range(len(x_seq))]
t_seq = [(1.-math.acos(-1+2*i/len(x_seq))/math.pi) for i in range(len(x_seq))]
#t_seq = [(i/len(x_seq))**2 for i in range(len(x_seq))]
t_seq_copy = [i+1. for i in t_seq]
t_seq.extend(t_seq_copy)
x_seq_copy = x_seq.copy()
x_seq.reverse()
x_seq.extend(x_seq_copy)
y_seq_copy = y_seq.copy()
y_seq.reverse()
y_seq.extend(y_seq_copy)


print("ln_x_seq:"+str(len(x_seq)))

class MoveAlongTXYZPath(Animation):
    def __init__(
        self,
        mobject: Mobject,
        ts,
        points,
        is_sorted:bool=False,
        suspend_mobject_updating: bool = False,
        **kwargs,
    ) -> None:
        assert np.all(ts>=0), "no negative t_values allowed"
        assert len(ts)==len(points), "vectors have to be the same length"

        # Sort if unsorted in t
        if not is_sorted:
            ts,points = map(np.array,zip(*sorted([*zip(ts,points)])))
        self.points = points
        run_time = np.max(ts)
        self.alphas = ts/run_time
        super().__init__( mobject, 
                          suspend_mobject_updating=suspend_mobject_updating,
                          run_time=run_time,
                          rate_func=linear,
                          **kwargs)

    def interpolate_mobject(self, alpha: float) -> None:
        index = np.searchsorted(self.alphas,alpha)
        point = self.points[index]
        self.mobject.move_to(point)

#class SquareToCircle(Slide):
class SquareToCircle(Scene):
    def construct(self):

        self.camera.background_color = WHITE #RED_C
        config.frame_width = 12
        config.frame_height = 12
        #config.pixel_width = 1080
        #config.pixel_height = 1080

        myTemplate = TexTemplate()
        myTemplate.add_to_preamble(r"\usepackage{mathrsfs}")

        # Use for making triple dot product
        # txt_1 = Tex(
        #     r"$\mathscr{H} \rightarrow \mathbb{H}$}",
        #     tex_template=myTemplate,
        #     font_size=144,
        # )

        ## Create graph to show stiffening effect
        pos_plot = 1*RIGHT+DOWN
        pos_bar = pos_plot+2.5*UP
        y_length = 3
        x_length = 4
        plot_y_scale = 1/y_length
        axes = Axes(x_range=[0, 1, 5], y_range=[0, plot_y_scale*y_length,5], x_length=x_length, y_length=y_length, color=BLACK,axis_config={'tip_shape': StealthTip,'tip_width':0.2,'tip_height':0.2,'color':BLACK,'stroke_color':BLACK,'fill_color':BLACK,'stroke_width':4}).shift(pos_plot)
        func = axes.plot(lambda x: math.log(x)**2/y_log_scaling, x_range=[x_ini, 1, 0.001],stroke_width=6, color=PURE_RED)
        # Labels for the x-axis and y-axis.
        # y_label = axes.get_y_axis_label(Tex(r"$(\text{ln}|F|)^2$",color=BLACK), edge=LEFT, direction=LEFT, buff=0.4)
        y_label = axes.get_y_axis_label(Tex(r"Force",color=BLACK), edge=LEFT, direction=LEFT, buff=0.4)
        # x_label = axes.get_x_axis_label(Tex(r"$|F|$",color=BLACK), edge=DOWN, buff = -0.6)
        x_label = axes.get_x_axis_label(Tex(r"$\leftarrow$ Compression",color=BLACK), edge=DOWN, buff = -0.6).shift(LEFT)
        axes_labels = VGroup(x_label, y_label)
        self.play(Create(axes,),Write(func),run_time=1)
        self.play(FadeIn(axes_labels))
        # self.play(Create(axes, func), rate_func=linear)
        
        point_input = np.vstack((np.array(x_seq)*x_length-0.5*x_length, np.array(y_seq)/plot_y_scale-0.5*y_length, np.array(y_seq)*0)).T+pos_plot
        dot_0 = Dot(point= point_input[0,:], color=PURE_BLUE)
        dot_0.set_z_index(1)
        
        compression_bar = Rectangle(height=1, width=x_length, color=GRAY_B, fill_opacity=1.0, stroke_width=0).shift(pos_bar)
        cover_bar = Rectangle(height=1.1, width=x_length, color=WHITE, fill_opacity=1., stroke_width=0).shift(pos_bar-np.array([x_length,0,0]))
        cover_bar.set_z_index(1)
        support = SVGMobject("hatch_long.svg",stroke_color=BLACK,stroke_width=4,fill_opacity=0.,height=1.1).align_to(cover_bar,RIGHT+UP)
        support.set_z_index(2)
        load = VGroup()
        for i in range(3):
            load += Arrow(start=i*UP/3.3+RIGHT, end=i*UP/3.3,stroke_width=10,max_stroke_width_to_length_ratio=10,max_tip_length_to_length_ratio=0.4,color=BLACK)
        load.next_to(compression_bar,aligned_edge=RIGHT)#.shift((1-3/3.3)*DOWN)

        bar_trace_line = Line(0*UP,5*DOWN,color=PURE_BLUE,stroke_width=1.2).align_to(compression_bar,UP+RIGHT).shift(0.5*UP)

        move_bar = VGroup(compression_bar,load,bar_trace_line)

        self.play(FadeIn(compression_bar,cover_bar,support,load,bar_trace_line,dot_0))
        point_input_bar = np.vstack((np.array(x_seq)*x_length-1*x_length+move_bar.get_center()[0]-pos_plot[0], np.array(y_seq)*0+move_bar.get_center()[1]-1.5, np.array(y_seq)*0)).T+pos_bar
        
        # plot_title = Tex("1D Compression", color=BLACK).shift(pos_bar+1.5*UP)
        # self.play(AddTextLetterByLetter(plot_title))

        # self.start_loop()
        self.play(MoveAlongTXYZPath(mobject=move_bar,ts=np.array(t_seq)*3,points=point_input_bar,is_sorted=True), MoveAlongTXYZPath(mobject=dot_0,ts=np.array(t_seq)*3,points=point_input,is_sorted=True))
        # self.end_loop()
        # self.next_slide()


        
# Cpoy output to the directory where manim-sideview can find it
filename = 'SquareToCircle.mp4'
# resultspath_old = './media/videos/potato/480p15'
resultspath_old = './media/videos/Compression_1D_plot/1080p60'
# resultspath_new = './media/videos/potato/1080p60'
resultspath_new = './media/videos/Compression_1D_plot/1080p60'
# if os.path.exists(resultspath_old+'/'+filename):
#     if not os.path.exists(resultspath_new): os.makedirs(resultspath_new)
#     shutil.copy(resultspath_old+'/'+filename,resultspath_new+'/'+filename)


