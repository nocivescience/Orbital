from manim import *
class ElectronScene(Scene):
    CONFIG={
        'center':ORIGIN+UP
    }
    def construct(self):
        self.get_dots(1,8)
        self.wait()
    def get_dots(self,radius,num):
        points=np.array([
            self.CONFIG['center']+rotate_vector(radius*RIGHT,theta)
            for theta in np.linspace(0,TAU,num)
        ])
        dots=VGroup()
        texts=VGroup()
        for i in range(len(points)):
            dot=Dot().move_to(points[i])
            text=MathTex('e_%g' %i)
            dot.text=text
            text.move_to(dot.get_center())
            vect=dot.get_center()-self.CONFIG['center']
            vect/=np.linalg.norm(vect)
            text.shift(vect*.4)
            texts.add(text)
            dots.add(dot)
        dots[0].set_opacity(0)
        texts[0].set_opacity(0)
        self.play(Create(dots),Write(texts))
        def update_dot(mob):
            mob.text.move_to(mob.get_center()) #poner .get_center()
            vect=mob.get_center()-self.CONFIG['center']
            vect/=np.linalg.norm(vect)
            mob.text.shift(vect*.4)
        for dot in dots:
            dot.add_updater(update_dot)
            curr_theta=angle_of_vector(dot.get_center()) #poner .get_center()
            new_theta=TAU*4+angle_of_vector(dot.get_center())
            def update_alpha(mob,alpha):
                theta=interpolate(curr_theta,new_theta,alpha)
                mob.move_to(
                    radius*np.cos(theta)*RIGHT+radius*np.sin(theta)*UP
                )
            self.play(
                UpdateFromAlphaFunc(dot,update_alpha),
                run_time=1
            )