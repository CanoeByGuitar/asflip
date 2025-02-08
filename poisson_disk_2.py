import taichi as ti
import taichi.math as tm

grid_n = 400
desired_samples = int(0.2 * 0.2 * grid_n * grid_n * 9)

sdf_center = ti.Vector([0.5, 0.45])
sdf_radius = 0.1
dx = 1 / grid_n
inv_dx = grid_n
grid = ti.field(dtype=int, shape=(grid_n, grid_n))
samples = ti.Vector.field(2, float, shape=desired_samples)
radius = dx * ti.sqrt(2)

def set_param():
    dx = 1 / grid_n
    inv_dx = grid_n
    grid = ti.field(dtype=int, shape=(grid_n, grid_n))
    samples = ti.Vector.field(2, float, shape=desired_samples)
    radius = dx * ti.sqrt(2)

@ti.func
def check_collision(p, index):
    x, y = index
    collision = False
    for i in range(max(0, x - 2), min(grid_n, x + 3)):
        for j in range(max(0, y - 2), min(grid_n, y + 3)):
            if grid[i, j] != -1:
                q = samples[grid[i, j]]
                if (q - p).norm() < radius - 1e-6:
                    collision = True
    return collision

@ti.kernel
def poisson_disk_sample() -> int:
    samples[0] = tm.vec2(0.5, 0.7)
    grid[int(grid_n * 0.5), int(grid_n * 0.7)] = 0
    head, tail = 0, 1
    while head < tail and head < desired_samples:
        source_x = samples[head]
        head += 1

        for _ in range(100):
            theta = ti.random() * 2 * tm.pi
            offset = tm.vec2(tm.cos(theta), tm.sin(theta)) * (1 + ti.random()) * radius
            new_x = source_x + offset
            new_index = int(new_x * inv_dx)

            if 0.4 <= new_x[0] < 0.6 and 0.65 <= new_x[1] < 0.85:
            # if (new_x - sdf_center).norm() < sdf_radius:
                collision = check_collision(new_x, new_index)
                if not collision and tail < desired_samples:
                    samples[tail] = new_x
                    grid[new_index] = tail
                    tail += 1
    return tail

a = poisson_disk_sample()
print("a:", a)

@ti.func
def PDSampleInCircleDartThrowing(dest_field, offset, center, radius, particle_num, r_threshold):
    next_particle = 0
    max_attempts = 100
    debug = 0
    while next_particle < particle_num:
        attemps = 0   
        while attemps < max_attempts:
            # gen random point
            theta = ti.random() * 2 * 3.14
            r = ti.random()
            x = ti.Vector([
            ti.cos(theta) * ti.sqrt(r) * radius + center[0],
            ti.sin(theta) * ti.sqrt(r) * radius + center[1]
            ])
        
            # check distance
            satisfy = True
            for i in range(next_particle):
                if (x - dest_field[i + offset]).norm() < r_threshold:
                    satisfy = False
                    break
            
            # add into list
            if satisfy or attemps > max_attempts - 2:
                dest_field[offset + next_particle] = x
                next_particle = next_particle + 1
                break
            
            attemps = attemps + 1
            debug = max(debug, attemps)
    return debug

# @ti.func
# def PDSampleInCircle(dest_field, offset, center, radius, particle_num, r_threshold):
    next_particle = 0
    max_attempts = 1000
    debug = 0
    while next_particle < particle_num:
        attemps = 0
        x = ti.Vector([0, 0])
        while attemps < max_attempts:
            # gen random point
            theta = ti.random() * 2 * 3.14
            r = ti.random()
            x = ti.Vector([
            ti.cos(theta) * ti.sqrt(r) * radius + center[0],
            ti.sin(theta) * ti.sqrt(r) * radius + center[1]
            ])
        
            # check distance
            satisfy = True
            for i in range(next_particle):
                if (x - dest_field[i + offset]).norm() < r_threshold:
                    satisfy = False
                    break
            
            attemps = attemps + 1
            debug = max(debug, attemps)
            if satisfy:
                break

        # add into list
        dest_field[offset + next_particle] = x
        next_particle = next_particle + 1
    return debug


