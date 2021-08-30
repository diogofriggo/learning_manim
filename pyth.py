# to generate the video:
#python -m manim pyth.py PythagorasTheorem -pl

#self.play(TransformFromCopy(x, y)) #x moves to y's position while turning into y

# \; - a thick space.
# \: - a medium space.
# \, - a thin space.
# \! - a negative thin space.

from manimlib.imports import *
from pathlib import Path
import pandas as pd
import numpy as np

# NOTE: READ LINE 59
class PythagorasTheorem(Scene):
    CUSTOM_QUALITY_CAMERA_CONFIG = {
        'frame_rate': 15,
    }

    CONFIG = {
        "square_scale": 2,
    }

    def construct(self):
        self.write_title()
        self.wait(1)
        self.show_creation_of_left_square_at_center()
        self.wait(1)
        self.assign_letter_to_sides_of_left_square()
        self.wait(1)
        self.move_left_square_from_center_to_left()
        self.wait(1)
        self.move_right_square_out_of_left_square_towards_right()
        self.wait(1)
        self.copy_triangles_from_left_to_right_square()
        self.wait(1)
        self.transform_letters()
        self.wait(1)
        self.highlight_squares()
        self.wait(1)
        self.copy_letters_into_final_formula()
        self.wait(3)

    def write_title(self):
        self.title = TextMobject("Demonstração do Teorema de Pitágoras")
        self.title.next_to(TOP + [-7, -1/2, 0])
        self.play(Write(self.title))

    def show_creation_of_left_square_at_center(self):
        self.left_square =  Square(color=WHITE)
        self.left_square.scale(self.square_scale)

        dots = [
            self.left_square.point_from_proportion(i * 4/16 + 1/16) #1/16, 5/16, 9/16, 13/16
            for i in range(4)
        ]
        dots_corners = [
            self.left_square.point_from_proportion(i * 1/4) #0, 1/4, 2/4, 3/4
            for i in range(4)
        ]

        fill_colors = [YELLOW, BLUE, YELLOW, BLUE]

        self.triangles = [
            Polygon(
                dots[i],         #| -1  2 0  |  2 1 0  | 1 -2 0 | -2 -1 0 |
                dots_corners[i], #| -2  2 0  |  2 2 0  | 2 -2 0 | -2 -2 0 |
                dots[i-1],       #| -2 -1 0  | -1 2 0  | 2  1 0 |  1 -2 0 |
                stroke_width=0,
                fill_opacity=0.7,
                fill_color=fill_colors[i],
            )
            for i in range(4)
        ]

        self.triangles_group = VGroup(*self.triangles)
        #print(dots)         #[array([-1.,  2.,  0.]), array([2., 1., 0.]), array([ 1., -2.,  0.]), array([-2., -1.,  0.])]
        #print(dots_corners) #[array([-2.,  2.,  0.]), array([2., 2., 0.]), array([ 2., -2.,  0.]), array([-2., -2.,  0.])]

        self.left_square_with_triangles_group = VGroup(self.left_square, self.triangles_group)

        self.play(
            DrawBorderThenFill(
                self.left_square_with_triangles_group
            )
        )

    def assign_letter_to_sides_of_left_square(self):
        self.a1 = TexMobject("a") #hipotenusa
        self.b1 = TexMobject("b") #cateto adjacente
        self.c1 = TexMobject("c") #cateto oposto
        self.a1.move_to(self.triangles[3].get_center() + [0, 2/6, 0])
        self.b1.move_to(self.triangles[3].get_center() + [-11/6, 0, 0])
        self.c1.move_to(self.triangles[3].get_center() + [-2/6, -5/6, 0])
        self.play(
            Write(self.a1),
            Write(self.b1),
            Write(self.c1),
        )

        self.wait(1)

        self.a2 = TexMobject("a") #hipotenusa
        self.b2 = TexMobject("b") #cateto adjacente
        self.c2 = TexMobject("c") #cateto oposto
        self.a2.move_to(self.triangles[2].get_center() + [-2/6, -1/6, 0])
        self.b2.move_to(self.triangles[2].get_center() + [0, -11/6, 0])
        self.c2.move_to(self.triangles[2].get_center() + [5/6, -1/6, 0])
        self.play(
            Write(self.a2),
            Write(self.b2),
            Write(self.c2),
        )

    def move_left_square_from_center_to_left(self):
        self.left_square_with_triangles_and_letters_group = VGroup(
            self.left_square_with_triangles_group,
            self.a1,
            self.b1,
            self.c1,
            self.a2,
            self.b2,
            self.c2,
        )
        self.play(
            ApplyMethod(
                self.left_square_with_triangles_and_letters_group.move_to,
                LEFT_SIDE + [3, 0, 0],
            )
        )

    def move_right_square_out_of_left_square_towards_right(self):
        self.right_square = self.left_square.copy()
        self.right_square.set_color(WHITE)
        self.play(
            ApplyMethod(
                self.right_square.move_to,
                RIGHT_SIDE + [-3, 5/16, 0],
            )
        )

    def copy_triangles_from_left_to_right_square(self):
        dots2 = [                               #1/16 7/16 11/16 13/16
            self.right_square.point_from_proportion(i * 1/4 + j * 1/16) #3.11111111 2.25 0 | 6.11111111 -0.75  0 | 3.11111111 -1.75 0 | 2.11111111 -0.75 0
            for i,j in zip(range(4),[1,3,3,1])
        ]

        dots_corners2 = [                       #0 1/4 2/4 3/4
            self.right_square.point_from_proportion(i * 1/4)            #2.11111111 2.25 0 | 6.11111111  2.25  0 | 6.11111111 -1.75 0 | 2.11111111 -1.75 0
            for i in range(4)
        ]

        middle = np.array([ #3.11111111 -0.75 0
            dots2[0][0],
            dots2[1][1],
            0
        ])

        #print(dots2)         #[array([3.11111111, 2.25, 0.]), array([6.11111111, -0.75,  0.]), array([3.11111111, -1.75,  0.]), array([2.11111111, -0.75,  0.])]
        #print(dots_corners2) #[array([2.11111111, 2.25, 0.]), array([6.11111111,  2.25, 0.]),  array([6.11111111, -1.75,  0.]), array([2.11111111, -1.75,  0.])]
        #print(middle)               #[3.11111111 -0.75 0.]

        self.all_rectangles = [
            Polygon(
                dots_corners2[i],
                dots2[i],
                middle,
                dots2[i-1],
            )
            for i in range(4)
        ]

        self.all_rectangles_group = VGroup(*self.all_rectangles)
        # rectancles: rectangles of the triangles
        self.rectangles = self.all_rectangles[0::2]
        # Big and small squares
        self.squares = self.all_rectangles[1::2]
        # IMPORTANT
        # use total_points = 3 if you are using the 3/feb release
        # use total_points = 4 if you are using the most recent release
        total_points = 4
        self.rect_dot = [
            [
                self.rectangles[i].points[total_points * j] for j in range(4)
            ]
            for i in range(2)
        ]

        self.triangles2 = [
            Polygon(
                rect[i+1],
                rect[i],
                rect[i-1],
                fill_opacity=0.7
            ) for rect in self.rect_dot
            for i in [0,2]
        ]

        self.triangles2_group = VGroup(*self.triangles2)

        self.b1_copy = self.b1.copy()
        self.c1_copy = self.c1.copy()
        self.b2_copy = self.b2.copy()
        self.c2_copy = self.c2.copy()
        self.right_triangle_with_letters = VGroup(self.triangles[2].copy(), self.b2_copy, self.c2_copy)
        self.left_triangle_with_letters = VGroup(self.triangles[3].copy(), self.b1_copy, self.c1_copy)

        self.play(
            ApplyMethod(self.triangles[0].copy().move_to, self.triangles2[0].get_center() + [0/32, -1/64, 0]),
            ApplyMethod(self.triangles[1].copy().move_to, self.triangles2[2].get_center() + [-1/64, 0, 0]),
            ApplyMethod(self.right_triangle_with_letters.move_to, self.triangles2[0].get_center() + [7/32, -7/32-1/64, 0]),
            ApplyMethod(self.left_triangle_with_letters.move_to, self.triangles2[2].get_center() + [-6/32-1/64, -7/32, 0]),
            run_time=3,
        )

        # self.play(
        #     ApplyMethod(self.triangles[0].copy().move_to, self.triangles2[0].get_center()),
        # )

    def transform_letters(self):

        self.bs = VGroup(self.b1_copy, self.b2_copy)
        self.cs = VGroup(self.c1_copy, self.c2_copy)
        self.b_squared = TexMobject('b^2')
        self.b_squared.move_to(self.squares[1].get_center() + [2/32, 1/32, 0])
        self.c_squared = TexMobject('c^2')
        self.c_squared.move_to(self.squares[0])

        self.asz = VGroup(self.a1, self.a2)
        self.a_squared = TexMobject('a^2')
        self.a_squared.move_to(self.left_square)

        self.play(
            Transform(self.asz, self.a_squared),
            Transform(self.bs, self.b_squared),
            Transform(self.cs, self.c_squared),
            FadeOut(self.b1),
            FadeOut(self.b2),
            FadeOut(self.c1),
            FadeOut(self.c2),
        )

    def highlight_squares(self):
        self.squares[1].move_to(self.squares[1].get_center() + [0, 1/128, 0]) #[1] is the small square

        self.tilted_square = self.squares[0].copy()
        self.tilted_square.move_to(self.left_square)
        self.tilted_square.rotate(-np.arcsin(1/np.sqrt(10)))
        self.tilted_square.scale(1.045)

        self.squares_group = VGroup(*self.squares, self.tilted_square)
        self.squares_group.set_color(WHITE)
        self.squares_group.set_opacity(0.7)
        self.squares_group.set_fill(GREEN)

        self.a_squared_copy = self.a_squared.copy()
        self.b_squared_copy = self.b_squared.copy()
        self.c_squared_copy = self.c_squared.copy()

        self.play(
            DrawBorderThenFill(self.squares_group),
            ApplyMethod(self.a_squared_copy.move_to, self.a_squared),
            ApplyMethod(self.b_squared_copy.move_to, self.b_squared),
            ApplyMethod(self.c_squared_copy.move_to, self.c_squared),
        )

    def copy_letters_into_final_formula(self):
        self.theorem = TexMobject('a^2', ' = ', 'b^2', ' + ', 'c^2')
        self.theorem.move_to(BOTTOM + [0, 1, 0])
        self.equal_sign = TexMobject(' = ')
        self.equal_sign.move_to(self.theorem[1])
        self.plus_sign = TexMobject(' + ')
        self.plus_sign.move_to(self.theorem[3])

        self.play(
            Write(self.equal_sign),
            Write(self.plus_sign),
            ApplyMethod(self.a_squared.move_to, self.theorem[0]),
            ApplyMethod(self.b_squared.move_to, self.theorem[2]),
            ApplyMethod(self.c_squared.move_to, self.theorem[4]),
            run_time=3,
        )

        self.a1_copy = TexMobject('a')
        self.a1_copy.move_to(self.triangles[3].get_center() + [0, 2/6, 0])

        self.play(
            FadeIn(self.a1_copy),
            FadeIn(self.b1),
            FadeIn(self.c1),
            run_time=2
        )
