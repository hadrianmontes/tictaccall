import time
import numpy as np
import math
import warnings


class TicTacCall:
    def __init__(self, call_function):
        self._call_function = call_function
        self._time_series = np.empty(0)
        self._values = np.empty(0)
        
    def run(self, timestep, duration, verbose=True):
        self._time_series = np.zeros(math.ceil(duration/timestep) + 1)
        self._values = np.zeros(math.ceil(duration/timestep) + 1)
        start_time = time.time()
        end_time = start_time + duration + timestep/2
        repetition = 0
        
        
        while time.time() < end_time:
            next_call = start_time + (repetition +1) * timestep
            now = time.time()
            value = self._call_function()
            self._values[repetition] = value
            self._time_series[repetition] = now
            if verbose:
                print(f"Time = {repetition*timestep}, value={value}")
            repetition += 1
            final = time.time()
            sleep_time = next_call - final
            if sleep_time < 0:
                warnings.warn("Skipping missing frame")
                continue
            time.sleep(next_call - now)
    @property
    def time_series(self):
        return self._time_series.copy()
    
    @property
    def values(self):
        return self._values.copy()
            
if __name__ == "__main__":
    import numpy as np
    import matplotlib.pyplot as plt
    
    def test_time():
        sleep = abs(np.random.normal(0.03,0.01))
        time.sleep(sleep)
        return sleep
    
    TIMESTEP = 0.1
    tic = TicTacCall(test_time)
    tic.run(TIMESTEP, 1000, verbose=True)
    times = np.array(tic._time_series)
    points = np.arange(times.shape[0]) * TIMESTEP
    plt.plot(points, points)
    plt.scatter(points, times - times[0])
    
    plt.figure()
    plt.hist(times[1:]- times[:-1], bins="auto")
    
    plt.show()
    