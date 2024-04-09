import numpy as np
from manim import *
from math import comb, factorial
from manim_slides import Slide
 
 
class Poisson(Slide):
  def construct(self):
    
    title = Tex("Legge di Poisson").to_edge(UP)

    
    def get_histogram(possible_outcomes):
      result = VGroup()
      ax = Axes(
        x_range=[0, possible_outcomes], 
        x_length=8,
        y_range=[0, 0.5],
        y_length=4,
        tips=False, 
      ) 
      x_nums = VGroup(
        *[
          Integer()
          .scale(0.75) 
          .set_value(k)
          .next_to(ax.c2p(k+0.5, 0), DOWN, buff=0.35)
          for k in range(possible_outcomes)
        ]
      )
      y_nums = VGroup()
      value = 0
      for i in range(6):
        num = (
          Integer(value, unit="\\%")
          .scale(0.5)
          .next_to(ax.c2p(0, i / 10), LEFT, buff=0.1)
        )
        value += 10
        y_nums.add(num)
      result.add(ax, x_nums, y_nums)
      result.to_edge(DL, buff=0.6)
      return result
 
 
    def get_binomial_bars(p,n,n_max):
      binomial_probabilities = np.array([ comb(n,k) * p**k * (1-p)**(n-k) for k in range(0,n_max+1) ])
      
      binomial_bars = VGroup()
      for x, prop in enumerate(binomial_probabilities):
        p1 = VectorizedPoint().move_to(histogram[0].c2p(x+1/8, 0))
        p2 = VectorizedPoint().move_to(histogram[0].c2p(x-1/8 + 1, 0))
        p3 = VectorizedPoint().move_to(histogram[0].c2p(x-1/8 + 1, prop))
        p4 = VectorizedPoint().move_to(histogram[0].c2p(x+1/8, prop))
        points = VGroup(p1, p2, p3, p4)
        bar = Rectangle().replace(points, stretch=True)
        bar.set_style(
          fill_color=[TEAL],
          fill_opacity=1,
          stroke_color=[TEAL],
          stroke_opacity=1
        )
        binomial_bars.add(bar)
      return binomial_bars
    
    def get_poisson_bars(l,n_max):
      poisson_probabilities = np.array([ np.exp(-l)*l**k/factorial(k) for k in range(0,n_max+1) ])
      
      binomial_bars = VGroup()
      for x, prop in enumerate(poisson_probabilities):
        p1 = VectorizedPoint().move_to(histogram[0].c2p(x+1/8, 0))
        p2 = VectorizedPoint().move_to(histogram[0].c2p(x-1/8 + 1, 0))
        p3 = VectorizedPoint().move_to(histogram[0].c2p(x-1/8 + 1, prop))
        p4 = VectorizedPoint().move_to(histogram[0].c2p(x+1/8, prop))
        points = VGroup(p1, p2, p3, p4)
        bar = Rectangle().replace(points, stretch=True)
        bar.set_style(
          fill_color=[YELLOW_A],
          fill_opacity=0.5,
          stroke_color=[YELLOW_A],
          stroke_opacity=0.5
        )
        binomial_bars.add(bar)
      return binomial_bars
    
    l = 4
    n_max = 15
    n = 5
    p = l/n
    
    histogram = get_histogram(possible_outcomes=n_max+1)
    binomial_bars = get_binomial_bars(p,n,n_max)
    poisson_bars = get_poisson_bars(4,n_max)
    poisson_bars.set_z_index(binomial_bars.z_index + 1)
    
    text = VGroup()
    text_average = Tex(f"Media: {l}").scale(0.6)
    text.add(text_average)
    text_success_probability = Tex("Probabilità di successo: ").scale(0.6)
    text.add(text_success_probability)
    text_number_of_trials = Tex("Numero di tentativi: ").scale(0.6)
    text.add(text_number_of_trials)
    text.arrange(DOWN, center=False, aligned_edge=LEFT)  
    text.to_edge(RIGHT, buff=1.6)
    success_probability = Tex(f"{p*100:.2f}").scale(0.6).next_to(text_success_probability, RIGHT)
    number_of_trials = Tex(f"{n}").scale(0.6).next_to(text_number_of_trials, RIGHT)

    

    def update(dummy,n,p):
      binomial_bars.become(get_binomial_bars(p,n,n_max))
      success_probability.become(Tex(f"{p*100:.2f}\%").scale(0.6).next_to(text_success_probability, RIGHT))
      number_of_trials.become(Tex(f"{n}").scale(0.6).next_to(text_number_of_trials, RIGHT))

    self.add(title, histogram, binomial_bars, poisson_bars, text, success_probability,number_of_trials)

    group = VGroup(binomial_bars,success_probability,number_of_trials)
    for n in range(5,10):
      p = l/n
      self.play(UpdateFromFunc(group, lambda m: update(m,n,p)), run_time=0.1) 
      self.next_slide()
    for n in range(10,201):
      p = l/n
      self.play(UpdateFromFunc(group, lambda m: update(m,n,p)), run_time=0.001) 
