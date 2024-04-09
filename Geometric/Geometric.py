import numpy as np
from manim import *
import random
from manim_slides import Slide
 
class Geometric(Slide):
  def construct(self):
    
    title = Tex("Legge geometrica").to_edge(UP)

    
    def get_histogram(possible_outcomes):
      result = VGroup()
      ax = Axes(
        x_range=[0, possible_outcomes], 
        x_length=8,
        y_range=[0, 0.6],
        y_length=4,
        tips=False, 
      ) 
      x_nums = VGroup(
        *[
          Integer()
          .scale(0.75) 
          .set_value(k)
          .next_to(ax.c2p(k+0.5, 0), DOWN, buff=0.35)
          for k in range(1,possible_outcomes)
        ]
      )
      y_nums = VGroup()
      value = 0
      for i in range(7):
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
    
    def generate_random_results(p,N):
      return np.random.geometric(p,N)
      
    def get_row(result): 
      nums = VGroup()
      for x in range(result-1):
        num = Integer(0)
        #num.set(height=0.25)
        #num.move_to(x * RIGHT)
        num.set_color(RED)
        num.to_edge(LEFT)
        nums.add(num)
      num = Integer(1)
      #num.set(height=0.25)
      #num.move_to((result-1) * RIGHT)
      num.set_color(GREEN)
      nums.add(num)
      
      nums.arrange(RIGHT)
      nums.next_to(title,DOWN,buff=0.6).to_edge(LEFT)
      row = VGroup(nums)
      row.nums = nums

      #row.center().next_to(title,DOWN,buff=0.6)
      return row
    
    def get_bars(histogram, data):
      portions = np.array(data).astype(float)
      total = portions.sum()
      if total == 0:
        portions[:] = 0
      else:
        portions /= total

      bars = VGroup()

      for x, prop in enumerate(portions):
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
        )
        bars.add(bar)
      return bars
    
    
    p = 0.2
    N = 400
    
    np.random.seed(42)
    results = generate_random_results(p,N)
    n_max = 21
    data = np.zeros((N,n_max+1))
    for i in range(N):
      k = results[i]
      data[i:,k] += 1
    histogram = get_histogram(possible_outcomes=n_max)
    row = get_row(results[0])
    bars = get_bars(histogram=histogram, data=data[0])

    text = VGroup()
    success_probability = Tex(f"Probabilità di successo: {p}").scale(0.6)
    text.add(success_probability)
    text_experiment_counter = Tex("Esperimento numero: ").scale(0.6)
    text.add(text_experiment_counter)
    text.arrange(DOWN, center=False, aligned_edge=LEFT)  
    text.to_edge(RIGHT, buff=0.8)
    experiment_counter = Tex(f"{0}").scale(0.6).next_to(text_experiment_counter, RIGHT)

     
    arrow = Line(ORIGIN, DOWN * 0.8).add_tip().set_color(TEAL)

    def update(dummy,new_row,new_data,i):
      row.become(new_row)
      bars.become(get_bars(histogram=histogram, data=new_data))
      arrow.next_to(bars[results[i]], UP, buff=0.1) 
      experiment_counter.become(Tex(f"{i+1}").scale(0.6).next_to(text_experiment_counter, RIGHT))

    self.add(title, histogram, row, bars, text, experiment_counter, arrow)

    group = VGroup(row, bars, arrow, experiment_counter)
    for i in range(1,10):
      new_row = get_row(results[i])
      new_data = data[i]
      self.play(UpdateFromFunc(group, lambda m: update(m,new_row,new_data,i)), run_time=0.1) 
      self.next_slide()
    self.next_slide()
    for i in range(10,20):
      new_row = get_row(results[i])
      new_data = data[i]
      self.play(UpdateFromFunc(group, lambda m: update(m,new_row,new_data,i)), run_time=0.1) 
      self.wait(0.5)
    self.next_slide()
    for i in range(20,400):
      new_row = get_row(results[i])
      new_data = data[i]
      self.play(UpdateFromFunc(group, lambda m: update(m,new_row,new_data,i)), run_time=0.001) 
