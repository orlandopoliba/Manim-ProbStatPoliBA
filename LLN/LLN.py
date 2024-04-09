import numpy as np
from manim import *
import random
from manim_slides import Slide
 
class LLN(Slide):
  def construct(self):
    
    title = Tex("Legge dei grandi numeri").to_edge(UP)
    
    shift_sample = 3*LEFT

    def generate_random_coordinates(N,r):
      xycoordinates = r*(2*np.random.rand(N,2)-1)
      coordinates = np.c_[xycoordinates, np.zeros(N)]
      return coordinates
      
    def get_points(coordinates,circle): 
      r = circle.radius
      N = coordinates.shape[0]
      successes = np.zeros(N, dtype=int)
      points = VGroup()
      for i, xyz in enumerate(coordinates):
        point = Dot(point=xyz)
        x = xyz[0]
        y = xyz[1]
        r2 = x**2 + y**2
        point.inside = r2 < r**2
        if point.inside: 
          point.set_color(GREEN)
          successes[i:] += 1
        else:
          point.set_color(RED)
        points.add(point)

      points.shift(shift_sample)
      return points, successes
    
    N = 10_000
    r = 2
    
    circle = Circle(radius=r, color=GREEN).shift(shift_sample)
    box = Rectangle(height=4,width=4, color=RED).shift(shift_sample)
     
    np.random.seed(42)
    sampled_coordinates = generate_random_coordinates(N,r)
    sampled_points, successes = get_points(sampled_coordinates[0:1],circle)
        
    text = VGroup()
    text_successes = Tex("Numero di successi: ").scale(0.6)
    text.add(text_successes)
    text_trials = Tex("Numero di tentativi: ").scale(0.6)
    text.add(text_trials)
    text.arrange(DOWN, aligned_edge=LEFT)  
    text.to_edge(RIGHT, buff=2)
    
    text_ratio = Tex(r"$\displaystyle 4 \frac{\text{Numero di successi}}{\text{Numero di tentativi}}$: ").scale(0.6).to_corner(DL)
 
    
    counters = VGroup()
    successes_counter = Tex(f"{successes[-1]}").scale(0.6).next_to(text_successes, RIGHT)
    counters.add(successes_counter)
    trials_counter = Tex(f"{1}").scale(0.6).next_to(text_trials, RIGHT)
    counters.add(trials_counter)
    ratio_counter = Tex(f"{4 * successes[-1]/1:.10f}").scale(0.6).next_to(text_ratio, RIGHT)
    counters.add(ratio_counter)
       
    text_pi = Tex(r"$\pi \simeq $" + f" {np.pi:.10f}").scale(0.6).next_to(ratio_counter, buff=1)

    animated_group = VGroup(sampled_points, counters)
    
    self.add(title, box, circle, animated_group, text, text_ratio, text_pi, counters)
    
    def update(dummy,i):
      new_points, new_successes = get_points(sampled_coordinates[:i,:],circle)
      sampled_points.become(new_points)
      successes_counter.become(Tex(f"{new_successes[-1]}").scale(0.6).next_to(text_successes, RIGHT))
      trials_counter.become(Tex(f"{i}").scale(0.6).next_to(text_trials, RIGHT))
      ratio_counter.become(Tex(f"{4 * new_successes[-1]/i:.10f}").scale(0.6).next_to(text_ratio, RIGHT))
      pass 
    
    for i in range(1,10):
      self.play(UpdateFromFunc(animated_group, lambda m: update(m,i)), run_time=0.1) 
      self.next_slide()  
    for i in range(10,100):
      self.play(UpdateFromFunc(animated_group, lambda m: update(m,i)), run_time=0.1)
    for k in range(1,10):
      self.play(UpdateFromFunc(animated_group, lambda m: update(m,100*k)), run_time=0.1)
    for k in range(1,10):
      self.play(UpdateFromFunc(animated_group, lambda m: update(m,1000*k)), run_time=0.1)

    self.wait() 