import { createRouter, createWebHistory } from 'vue-router'
import Index from '../views/Index.vue'
import About from '../views/About.vue'
import derivativeSolver from "../views/DerivativeSolver.vue";
import integralSolver from "../views/IntegralSolver.vue";
import parabolic1DSolver from "../views/Parabolic1DSolver.vue";
import parabolic2DSolver from "../views/Parabolic2DSolver.vue";
import fractionalParabolicSolver from "../views/FractionalParabolicSolver.vue";
import inverseParabolicSolver from "../views/InverseParabolicSolver.vue";
import hyperbolicSolver from "../views/Hyperbolic1DSolver.vue";
import elliptic1DSolver from "../views/Elliptic1DSolver.vue";
import elliptic2DSolver from "../views/Elliptic2DSolver.vue";
import inverseEllipticSolver from "../views/InverseEllipticSolver.vue";
import odeFirstOrderSolver from "../views/OdeFirstOrderSolver.vue";
import odeSecondOrderSolver from "../views/OdeSecondOrderSolver.vue";
import nonlinearSolver from "../views/NonlinearSolver.vue";
import wastewaterSolver from "../views/WastewaterSolver.vue";
import stgSolver from "../views/stgSolver.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
      {
          path: '/',
          name: 'Home',
          component: Index
      },
      {
          path: '/about',
          name: 'About',
          component: About
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
          path: "/elliptic-1d",
          name: 'Elliptic1DSolver',
          component: elliptic1DSolver,
      },
      {
          path: "/elliptic-2d",
          name: 'Elliptic2DSolver',
          component: elliptic2DSolver,
      },
      {
          path: "/inverse-elliptic",
          name: 'InverseElliptic',
          component: inverseEllipticSolver,
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
      {
          path: "/stg-solver",
          name: 'STGSolver',
          component: stgSolver,
      },
      {
          path: "/wastewater-solver",
          name: 'WastewaterSolver',
          component: wastewaterSolver,
      },
  ],
})

export default router
