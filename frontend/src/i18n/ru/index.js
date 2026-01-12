import menu from './menu'
import derivative from './derivative'
import definiteIntegral from './definiteIntegral'
import parabolic1d from './parabolic1D.js'
import parabolic2d from './parabolic2D.js'
import fractionalParabolic1D from './fractionalParabolic1D.js'
import inverseParabolic1D from './inverseParabolic1D'
import hyperbolic1D from './hyperbolic1D'
import elliptic1D from './elliptic1D'
import elliptic2D from './elliptic2D'
import inverseElliptic1D from './inverseElliptic1D'
import odeFirstOrder from './odeFirstOrder'
import odeSecondOrder from './odeSecondOrder'
import wastewater from './wastewater'
import stg from './stg'
import nonlinearEquation from './nonlinearEquation'

export default {
    menu,
    derivative,
    definiteIntegral,
    parabolic1d,
    parabolic2d,
    fractionalParabolic1D,
    inverseParabolic1D,
    hyperbolic1D,
    elliptic1D,
    elliptic2D,
    inverseElliptic1D,
    odeFirstOrder,
    odeSecondOrder,
    wastewater,
    stg,
    nonlinearEquation,

    index: {
        derivatives: 'Производные',
        integrals: 'Интегралы',
        definiteIntegral: 'Определенный интеграл',
        fractionalIntegral: 'Дробный интеграл',
        parabolicEquations: 'Параболические уравнения',
        oneDim: 'Одномерное',
        twoDim: 'Двумерное',
        withFractionalDerivative: 'С дробным производным',
        inverseProblem: 'Обратная задача',
        hyperbolicEquations: 'Гиперболические уравнения',
        ellipticEquations: 'Эллиптические уравнения',
        ordinaryDifferentialEquations: 'Обыкновенные дифференциальные уравнения',
        firstOrderDifferentialEquation: 'Дифференциальное уравнения первого порядка',
        secondOrderDifferentialEquation: 'Дифференциальное уравнение второго порядка',
        otherEquations: 'Другие уравнения',
        wastewater: 'Численное моделирование процесса биологической очистки сточных вод',
        solidTumorGrowth: 'Модель роста солидной опухоли',
        nonlinearEquation: 'Нелинейное уравнение',
    }
}