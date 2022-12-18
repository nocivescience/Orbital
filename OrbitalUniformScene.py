from manim import *
class Orbitals(Scene):
    CONFIG={
        "center":ORIGIN,
        "radius":[1,2,3],
        "numbers":[2,8,8],
        "dot_style":{
            "radius":0.08,
            "color":interpolate_color(RED,YELLOW,np.random.random())
        },
        "dot_center_style":{
            "color":WHITE,
            "radius":0.2,
        }
    }

    def construct(self):
        self.get_circle(self.CONFIG['radius'])
        mobs=VGroup()
        for t in range(len(self.CONFIG['radius'])):
            mob=self.get_points(self.CONFIG['radius'][t],num=self.CONFIG['numbers'][t])
            mobs.add(mob)
        textos=VGroup()
        for t in range(len(self.CONFIG['radius'])):
            texto=self.get_labels(mobs[t],t)
            textos.add(texto)
        self.play(*list(map(Create,[mobs])),run_time=4)
        self.play(LaggedStartMap(Write,textos))
        self.wait()
        time=0
        while time<15:
            pre_time=2
            time+=pre_time
            self.play(
                *[self.get_ubication_points(t,self.CONFIG['radius'][0],np.random.uniform(0,2*np.pi)) for t in mobs[0]],
                *[self.get_ubication_points(t,self.CONFIG['radius'][1],np.random.uniform(0,2*np.pi)) for t in mobs[1]],
                *[self.get_ubication_points(t,self.CONFIG['radius'][2],np.random.uniform(0,2*np.pi)) for t in mobs[2]],
                *[self.get_labels_update(mobs[t],textos[t]) for t in range(len(self.CONFIG['radius']))],
                run_time=pre_time,
                rate_func=double_smooth
            )

    def get_points(self,radius,num):
        points=np.array([
            self.CONFIG['center']+rotate_vector(radius*RIGHT,theta) for theta in np.random.uniform(0,2*np.pi,num)
        ])
        dots=VGroup()
        for point in points:
            dot=Dot(**self.CONFIG['dot_style']).move_to(point)
            dots.add(dot)
        return dots
    
    def get_circle(self,radius):
        dot_center=Dot(self.CONFIG['center'],**self.CONFIG['dot_center_style'])
        texto=MathTex("+").move_to(dot_center.get_center())
        texto.set_color(BLACK).set_stroke(width=1,color=BLACK)
        texto.set_width(dot_center.get_width())
        dot_center.add(texto)
        self.add_foreground_mobjects(dot_center,texto)
        self.play(Create(dot_center))
        for radio in radius:
            radii=DashedLine(dot_center.get_center(),RIGHT*radio)
            self.play(Create(radii))
            circle=Circle(color=BLUE,radius=radio)
            self.play(Rotate(radii,angle=TAU,about_point=dot_center.get_center())\
                ,Create(circle),run_time=1,rate_func=smooth)
            self.play(Create(radii,rate_func=lambda t: 1-t))
        self.wait()

    def get_ubication_points(self,mob,radius,theta):
        curr_theta=angle_of_vector(mob.get_center())
        new_theta=(curr_theta+theta)%(2*np.pi)-2*np.pi
        def get_update(mob,alpha):
            theta=interpolate(curr_theta,new_theta,alpha)
            mob.move_to(radius*(np.cos(theta)*RIGHT+np.sin(theta)*UP))
            return mob
        return UpdateFromAlphaFunc(mob,get_update)
    
    def get_labels(self,mobs,m):
        point_labels=VGroup()
        for t,mob in zip(range(self.CONFIG['numbers'][m]),mobs):
            point_label=MathTex("e_%i" %(t+1)).scale(0.6)
            point_label.move_to(mob)
            vect=mob.get_center()-self.CONFIG['center']
            vect/=np.linalg.norm(vect)
            point_label.shift(vect*0.26)
            point_labels.add(point_label)
        return point_labels

    def get_labels_update(self,point_mobs,labels):
        def update_labels(labels):
            for label, mob in zip(labels,point_mobs):
                label.move_to(mob)
                vect=mob.get_center()-self.CONFIG['center']
                vect/=np.linalg.norm(vect)
                label.shift(vect*0.26)
            return label
        return UpdateFromFunc(labels,update_labels)