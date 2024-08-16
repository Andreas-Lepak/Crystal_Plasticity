from manim import *
# from manim.opengl import *
#from manim_slides import Slide
# from manim_meshes import *
# from moderngl import *
# import cv2
import os, sys, subprocess, time, shutil
# import math
import numpy as np

# Render slides:
# manim potato.py --disable_caching -pqh --fps=30
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
# manim potato.py --disable_caching -p

#class SquareToCircle(Slide):
class SquareToCircle(Scene):
    def construct(self):

        # self.camera.background_color = WHITE #RED_C

        myTemplate = TexTemplate()
        myTemplate.add_to_preamble(r"\usepackage{mathrsfs}")

        # Use for making triple dot product
        # txt_1 = Tex(
        #     r"$\mathscr{H} \rightarrow \mathbb{H}$}",
        #     tex_template=myTemplate,
        #     font_size=144,
        # )

        potato_pos = 0*RIGHT+DOWN

        half_circle = Arc(fill_opacity=1, angle=-PI,color=BLACK).shift(3*UP+potato_pos)
        bed = Rectangle(height=1, width=4, color=BLACK, fill_opacity=1.).shift(0.5*UP+potato_pos)
        boundary = Rectangle(height=3, width=4, color=BLACK, fill_color=GRAY_B, fill_opacity=1.).align_to(bed,DOWN+LEFT)
        boundary.set_z_index(-1)
        potato_1 = SVGMobject("potato_v4.svg",stroke_color=BLACK,fill_opacity=1.0, fill_color=BLACK).shift(3*UP+potato_pos)
        potato_2 = SVGMobject("potato_v5.svg",stroke_color=BLACK,fill_opacity=1.0, fill_color=BLACK).shift(0.0*UP+potato_pos)
        potato_3 = SVGMobject("potato_v6.svg",stroke_color=BLACK,fill_opacity=1.0, fill_color=GRAY_B,stroke_width=3).shift(1.2*UP+potato_pos).scale(3.5)
        potato_3.set_z_index(-1)
        # txt_1 = Tex(r"$\mathcal{B}_1$",color=WHITE).move_to(potato_1)
        txt_1 = Tex(r"Solid",color=WHITE).move_to(potato_1)
        txt_1.generate_target()
        txt_1.target.move_to(half_circle)
        # txt_2 = Tex(r"$\mathcal{B}_2$",color=WHITE).move_to(potato_2)
        txt_2 = Tex(r"Solid",color=WHITE).move_to(potato_2)
        txt_2.generate_target()
        txt_2.target.move_to(bed)
        # txt_3 = Tex(r"$\mathcal{B}_3$",color=BLACK).move_to(potato_3)
        txt_3 = Tex(r"Third medium",color=BLACK).move_to(potato_3)
        txt_3.generate_target()
        txt_3.target.move_to(boundary)

        ## Draw and fill potatoes + add body text
        self.play(DrawBorderThenFill(potato_1),DrawBorderThenFill(potato_2))
        # self.play(Write(txt_1),Write(txt_2))
        self.play(FadeIn(txt_1),FadeIn(txt_2))
        # self.next_slide()

        self.play(DrawBorderThenFill(potato_3))
        # self.play(Write(txt_3))
        self.play(FadeIn(txt_3))
        # self.next_slide()

        ## Transform potatoes to Hertz
        self.wait()
        self.play(ReplacementTransform(potato_1,half_circle),ReplacementTransform(potato_2,bed),ReplacementTransform(potato_3,boundary),MoveToTarget(txt_1),MoveToTarget(txt_2),MoveToTarget(txt_3))
        self.wait(1)

        ## Fade out everything
        # self.play(
        #     *[FadeOut(mob)for mob in self.mobjects]
        #     # All mobjects in the screen are saved in self.mobjects
        # )

        
# Cpoy output to the directory where manim-sideview can find it
filename = 'SquareToCircle.mp4'
resultspath_old = './media/videos/potato/480p15'
# resultspath_new = './media/videos/potato/1080p60'
# if os.path.exists(resultspath_old+'/'+filename):
#     if not os.path.exists(resultspath_new): os.makedirs(resultspath_new)
#     shutil.copy(resultspath_old+'/'+filename,resultspath_new+'/'+filename)


