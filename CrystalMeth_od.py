from tkinter import CENTER
from turtle import width
from manim import *
# from manim.opengl import *
#from manim_slides import Slide
# from manim_meshes import *
# from moderngl import *
# import cv2
import os, sys, subprocess, time, shutil
# import math
from manim.mobject.svg.svg_mobject import SVGMobject
import numpy as np

# Render slides:
# manim potato.py --disable_caching -pqh --fps=30
# Play slides
# manim-slides HuHu_reg --start-paused -r 1280 720
# Convert slides to HTML
# manim-slides convert HuHu_reg --open HTML_slides_v2

# Convert slides to pptx
# manim-slides convert --to=pptx HuHu_reg pptx_slides.pptx

# Configure keys for slides
# manim-slides wizard

# Render with opengl
# manim -qm -p --renderer=opengl test_manim.py HuHu_reg

# Render with setting from config files (remoe flags which overwrite properties)
# manim potato.py --disable_caching -p

class CrystalMeth_od_Scene(Scene):

    def __init__(self, **kwargs):
        # initialize the vmobject
        super().__init__(**kwargs)

        Mobject.set_default(color=BLACK)

        # Add stuff to Latex preamble
        self.myTemplate = TexTemplate()
        self.myTemplate.add_to_preamble(r"\usepackage[scaled]{helvet}")
        self.myTemplate.add_to_preamble(r"\renewcommand\familydefault{\sfdefault} ")
        self.myTemplate = TexTemplate()
        self.myTemplate.add_to_preamble(r"\usepackage{mathrsfs}")
        self.myTemplate.add_to_preamble(r"""\usepackage{tikz,pgfplots}
            \usepgfplotslibrary{patchplots}
            \usepgfplotslibrary{colormaps}
            \pgfplotsset{compat=1.18}
            \DeclareUnicodeCharacter{2212}{−}
            \usepgfplotslibrary{groupplots,dateplot}""")
        self.myTemplate.add_to_preamble(r"""\newcommand{\tripledot}{%      
            \tikz[baseline=-0.2ex]{ \draw[black,fill=black] (0,0) circle (.1ex); 
            \draw[black,fill=black] (0,0.6ex) circle (.1ex); 
            \draw[black,fill=black] (0,1.2ex) circle (.1ex) }%  
            }""")       
        self.myTemplate.add_to_preamble(r"\usepackage[T1]{fontenc}")
 
        
        # Fontsizes
        self.font_size_title = 60
        self.font_size_subtitle = 50
        self.font_size_text = 30
        self.font_size_author = 30
        self.font_size_footer = 20
        self.font_size_caption = 20

        # DTU red
        self.DTU_RED = '#990000' 
        self.color_theme = self.DTU_RED

    def construct(self):

        vr_scale = 1.7
        vr_shift = 2*RIGHT

        vr_1 = SVGMobject("Material/crystal_plast_def0.svg").scale(vr_scale)
        vr_2 = SVGMobject("Material/crystal_plast_def_plast.svg").scale(vr_scale)
        vr_3 = SVGMobject("Material/crystal_plast_def_plast_left.svg").scale(vr_scale)

        # vr_1.set_opacity(1.)
        # vr_2.set_opacity(1.)
        # vr_1[0].set_fill_color(WHITE)
        # vr_2[0].set_fill_color(WHITE)

        # vr_1.set_stroke(width=4,color=BLACK)
        # vr_2.set_stroke(width=4,color=BLACK)

        vr_1.remove(vr_1[-1],vr_1[-2]).set_stroke(width=2,color=BLACK)
        vr_2.remove(vr_2[-1],vr_2[-2]).set_stroke(width=2,color=BLACK)
        vr_3.remove(vr_3[-1],vr_3[-2]).set_stroke(width=2,color=BLACK)

        vr_1c = vr_1.copy()

        for i in range(6):
            # vr_1[1+i].set_fill_color(WHITE)
            # vr_1[1+i].set_z(2)
            vr_1c[-i-1].set_stroke(width=4,color=PURE_BLUE)
            vr_2[-i-1].set_stroke(width=4,color=PURE_BLUE)
            vr_3[-i-1].set_stroke(width=4,color=PURE_BLUE)
            # vr_1[1-i].set_fill_color(PURE_BLUE)

        
        # for i in range(9):
        #     vr_2[1+i].set_fill_color(PURE_RED)
        #     vr_2[1+i].set_stroke(width=2,color=BLACK)
        #     vr_2[1+i].set_z(3)
        
        # vr_1c = vr_1.copy()
        # for i in range(9):
        #     vr_1c[1+i].set_z(2)
        #     vr_1c[1+i].set_opacity(1.)
        #     vr_1c[1+i].set_fill_opacity(0.)

        vr_1cc = vr_1c.copy()

        punkt = 0.845*DOWN+1.0*LEFT
        arrow_s0 = Arrow(start= punkt , end=punkt+0.8*RIGHT, stroke_width=4, color=PURE_BLUE,max_tip_length_to_length_ratio=0.3, max_stroke_width_to_length_ratio=8,buff=0.)#.shift(0.845*DOWN+0.72*LEFT)
        arrow_n0 = Arrow(start= punkt , end=punkt+0.8*UP,    stroke_width=4, color=BLACK,max_tip_length_to_length_ratio=0.3, max_stroke_width_to_length_ratio=8,buff=0.)#.shift(0.845*DOWN+0.72*LEFT)
        

        txt_vr_1 = Tex(r"$\mathbf{s}_0$",   color=PURE_BLUE, font_size = self.font_size_text).move_to(vr_1.get_center(),DOWN).shift(0.2*UP)
        txt_vr_2 = Tex(r"$\mathbf{n}_0$",   color=BLACK,     font_size = self.font_size_text).move_to(vr_1.get_center(),DOWN)

        txt_vr_1.move_to(punkt+0.3*(DOWN+RIGHT),LEFT)
        txt_vr_2.move_to(punkt+0.3*(UP+LEFT))

        # Part 1
        self.play(DrawBorderThenFill(vr_1))
        self.play(Create(arrow_s0),Create(arrow_n0))
        self.play(Create(txt_vr_1),Create(txt_vr_2))
        self.add(txt_vr_1)#,FadeIn(vr_1c))
        self.wait(0.1)
        self.play(ReplacementTransform(vr_1,vr_1c))

        # Part 2
        # self.add(vr_1c,txt_vr_1,txt_vr_2,arrow_s0,arrow_n0)
        self.play(ReplacementTransform(vr_1c,vr_2))
        self.wait(1)
        self.play(ReplacementTransform(vr_2,vr_3))
        self.wait(1)
        self.play(ReplacementTransform(vr_3,vr_1cc))
        self.wait(1)



        ## Fade out everything
        # self.play(
        #     *[FadeOut(mob)for mob in self.mobjects]
        #     # All mobjects in the screen are saved in self.mobjects
        # )

        
# Cpoy output to the directory where manim-sideview can find it
filename = 'GaussLobatto.mp4'

# resultspath_old = './media/videos/HuHu_reg/480p15'
# resultspath_new = './media/videos/potato/1080p60'
# if os.path.exists(resultspath_old+'/'+filename):
#     if not os.path.exists(resultspath_new): os.makedirs(resultspath_new)
#     shutil.copy(resultspath_old+'/'+filename,resultspath_new+'/'+filename)


