module fractals

   implicit none

   ! integer(8) :: pow = 2
   ! real(8) :: fac = 0.5

contains

   subroutine julia(x, nx, y, ny, c, max_iter, out)

      implicit none

      integer(8), intent(in) :: max_iter
      integer(8), intent(in) :: nx, ny
      real(8), intent(in) :: x(nx), y(ny)
      integer(8), dimension(nx, ny), intent(out) :: out
      complex(8), intent(in) :: c

      integer(8) :: i, j, k
      complex(8) :: z

      out = 0
      !$OMP PARALLEL DO PRIVATE(i, j, k, z)
      do j = 1, ny
         do i = 1, nx
            z = cmplx(x(i), y(j), kind=8)
            do k = 1, max_iter
               z = z**2 + c
               if (abs(z) > 2) then
                  out(i, j) = k
                  exit
               end if
            end do
         end do
      end do
      !$OMP END PARALLEL DO

   end subroutine julia

   subroutine mandelbrot_fractional(x, nx, y, ny, c, max_iter, pow, fac, out)

      implicit none

      integer(8), intent(in) :: max_iter
      integer(8), intent(in) :: nx, ny, pow
      real(8), intent(in) :: x(nx), y(ny), fac
      integer(8), dimension(nx, ny), intent(out) :: out
      complex(8), intent(in) :: c

      integer(8) :: i, j, k
      complex(8) :: z, w

      ! print *, pow, fac

      out = 0
      !$OMP PARALLEL DO PRIVATE(i, j, k, z)
      do j = 1, ny
         do i = 1, nx
            call mandelbrot_single_powfac(x(i), y(j), c, max_iter, pow, fac, out(i, j))
            ! z = cmplx(x(i), y(j), kind=8)
            ! w = c
            ! do k = 1, max_iter
            !    w = w**pow + fac*z ! Sale chulo
            !    if (abs(w) > 2) then
            !       out(i, j) = k
            !       exit
            !    end if
            ! end do
         end do
      end do
      !$OMP END PARALLEL DO

   end subroutine mandelbrot_fractional

   subroutine mandelbrot(x, nx, y, ny, c, max_iter, out)

      implicit none

      integer(8), intent(in) :: max_iter
      integer(8), intent(in) :: nx, ny
      real(8), intent(in) :: x(nx), y(ny)
      integer(8), dimension(nx, ny), intent(out) :: out
      complex(8), intent(in) :: c

      integer(8) :: i, j, k
      complex(8) :: z, w

      out = 0
      !$OMP PARALLEL DO PRIVATE(i, j, k, z)
      do j = 1, ny
         do i = 1, nx
            call mandelbrot_single(x(i), y(j), c, max_iter, out(i, j))
            ! z = cmplx(x(i), y(j), kind=8)
            ! w = c
            ! do k = 1, max_iter
            !    w = w**2 + z
            !    if (abs(w) > 2) then
            !       out(i, j) = k
            !       exit
            !    end if
            ! end do
         end do
      end do
      !$OMP END PARALLEL DO

   end subroutine mandelbrot

   subroutine fractal_4d(x, y, z, w, c, nx, ny, nz, max_iter, out)

      implicit none

      integer, intent(in) :: nx, ny, nz, max_iter
      real, intent(in) :: x(nx), y(ny), z(nz), w, c(4)
      real, intent(out) :: out(nz*ny*nx, 4)
      real :: q(4)
      integer :: i, j, k, l, n

      out = 0.
      n = 1
      ! $OMP PARALLEL DO PRIVATE(q, i, j, k, n)
      do i = 1, size(x)
         do j = 1, size(y)
            do k = 1, size(z)
               q = [x(i), y(j), z(k), w]
               do l = 1, max_iter
                  q = q_mult(q, q) + c
                  if (q_norm(q) > 4) then
                     out(n, :) = [x(i), y(j), z(k), real(l)]
                     n = n + 1
                     exit
                     n = n + 1
                  end if
               end do
            end do
         end do
      end do
      ! $OMP END PARALLEL DO

   contains

      function q_mult(a, b) result(c)
         real, intent(in) :: a(4), b(4)
         real :: c(4)

         c(1) = a(1)*b(1) - a(2)*b(2) - a(3)*b(3) - a(4)*b(4)
         c(2) = a(1)*b(2) + a(2)*b(1) + a(3)*b(4) - a(4)*b(3)
         c(3) = a(1)*b(3) - a(2)*b(4) + a(3)*b(1) + a(4)*b(2)
         c(4) = a(1)*b(4) + a(2)*b(3) - a(3)*b(2) + a(4)*b(1)

      end function q_mult

      function q_norm(a) result(b)
         real :: a(4)
         real :: b

         b = sqrt(sum(q_mult(a, a)))

      end function q_norm

   end subroutine fractal_4d

   subroutine mandelbrot_single_powfac(x, y, c, max_iter, pow, fac, out)
      real(8), intent(in) :: x, y, fac
      integer(8), intent(in) :: max_iter, pow
      complex(8), intent(in) :: c
      integer(8), intent(inout) :: out
      complex(8) :: z, w
      integer(8) :: k

      z = cmplx(x, y, kind=8)
      w = c
      do k = 1, max_iter
         w = w**pow + fac*z
         if (abs(w) > 2) then
            out = k
            exit
         end if
      end do
   end subroutine mandelbrot_single_powfac

   subroutine mandelbrot_single(x, y, c, max_iter, out)
      real(8), intent(in) :: x, y
      integer(8), intent(in) :: max_iter
      complex(8), intent(in) :: c
      integer(8), intent(inout) :: out
      complex(8) :: z, w
      integer(8) :: k

      z = cmplx(x, y, kind=8)
      w = c
      do k = 1, max_iter
         w = w**2 + z
         if (abs(w) > 2) then
            out = k
            exit
         end if
      end do
   end subroutine mandelbrot_single

end module fractals
