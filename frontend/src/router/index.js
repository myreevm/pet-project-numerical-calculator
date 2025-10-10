import { createRouter, createWebHistory } from 'vue-router'
import Index from '../views/Index.vue'
import derivativeSolver from "../views/DerivativeSolver.vue";
import integralSolver from "../views/IntegralSolver.vue";
import parabolic1DSolver from "../views/Parabolic1DSolver.vue";
import parabolic2DSolver from "../views/Parabolic2DSolver.vue";
import fractionalParabolicSolver from "../views/FractionalParabolicSolver.vue";
import inverseParabolicSolver from "../views/InverseParabolicSolver.vue";
import hyperbolicSolver from "../views/Hyperbolic1DSolver.vue";
import ellipticSolver from "../views/EllipticSolver.vue";
import odeFirstOrderSolver from "../views/OdeFirstOrderSolver.vue";
import odeSecondOrderSolver from "../views/OdeSecondOrderSolver.vue";
import nonlinearSolver from "../views/NonlinearSolver.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
      {
          path: '/',
          name: 'Home',
          component: Index
      },
      {
          path: '/derivative-solver',
          name: 'DerivativeSolver',
          component: derivativeSolver
      },
      {
          path: '/integral-solver',
          name: 'IntegralSolver',
          component: integralSolver
      },
      {
          path: '/parabolic-1d',
          name: 'Parabolic_1d',
          component: parabolic1DSolver
      },
      {
          path: '/parabolic-2d',
          name: 'Parabolic_2d',
          component: parabolic2DSolver
      },
      {
          path: '/fractional-parabolic',
          name: 'FractionalParabolic',
          component: fractionalParabolicSolver
      },
      {
          path: '/inverse-parabolic',
          name: 'InverseParabolic',
          component: inverseParabolicSolver
      },
      {
          path: "/hyperbolic-1d",
          name: 'Hyperbolic1DSolver',
          component: hyperbolicSolver,
      },
      {
          path: "/elliptic-solver",
          name: 'EllipticSolver',
          component: ellipticSolver,
      },
      {
          path: "/odefirstorder-solver",
          name: 'OdeFirstOrderSolver',
          component: odeFirstOrderSolver,
      },
      {
          path: "/odesecondorder-solver",
          name: 'OdeSecondOrderSolver',
          component: odeSecondOrderSolver,
      },
      {
          path: "/nonlinear-solver",
          name: 'NonlinearSolver',
          component: nonlinearSolver,
      },
  ],
})

export default router
