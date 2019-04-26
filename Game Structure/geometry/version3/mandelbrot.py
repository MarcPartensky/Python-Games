import numpy as np

"""Still not operational."""

class Mandelbrot:
    def __init__(self,maxiter=200,horizon=2.0**40,precision=[1500,1250]):
        self.maxiter=maxiter
        self.horizon=horizon
        self.precision=precision

    def getMatrices(self,corners):
        xmin,ymin,xmax,ymax=corners
        xn,yn=self.precision
        X = np.linspace(xmin, xmax, xn, dtype=np.float32)
        Y = np.linspace(ymin, ymax, yn, dtype=np.float32)
        C = X + Y[:, None]*1j
        N = np.zeros(C.shape, dtype=int)
        Z = np.zeros(C.shape, np.complex64)
        for n in range(self.maxiter):
            I = np.less(abs(Z),self.horizon)
            N[I] = n
            Z[I] = Z[I]**2 + C[I]
        N[N==self.maxiter-1] = 0
        return Z, N

    def correct(self,Z,N):
        log_horizon=np.log(np.log(self.horizon))/np.log(2)
        with np.errstate(invalid='ignore'):
            M = np.nan_to_num(N+1-np.log(np.log(abs(Z)))/np.log(2)+log_horizon)
        return M

    def show(self,surface):
        corners=surface.getCorners()
        Z,N=self.getMatrices(corners)
        M=self.correct(Z,N)


if __name__=="__main__":
    from mysurface import Surface
    surface=Surface()
    set=Mandelbrot()
    set.show(surface)
