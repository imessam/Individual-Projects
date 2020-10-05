/*
 * File: Subsystem.c
 *
 * Code generated for Simulink model 'Subsystem'.
 *
 * Model version                  : 1.1
 * Simulink Coder version         : 8.13 (R2017b) 24-Jul-2017
 * C/C++ source code generated on : Sat Jun 13 14:36:13 2020
 *
 * Target selection: ert.tlc
 * Embedded hardware selection: NXP->Cortex-M4
 * Code generation objectives:
 *    1. Execution efficiency
 *    2. RAM efficiency
 * Validation result: Not run
 */

#include "Subsystem.h"

/* Block signals and states (auto storage) */
DW rtDW;

/* External inputs (root inport signals with auto storage) */
ExtU rtU;

/* External outputs (root outports fed by signals with auto storage) */
ExtY rtY;

/* Real-time model */
RT_MODEL rtM_;
RT_MODEL *const rtM = &rtM_;

/* Model step function */
void Subsystem_step(void)
{
  real_T uSz_tmp;

  /* DiscreteFilter: '<S1>/1//S(z)' incorporates:
   *  DiscreteFilter: '<S1>/R(z)'
   *  DiscreteFilter: '<S1>/T(z)'
   *  Inport: '<Root>/In1'
   *  Inport: '<Root>/In2'
   *  Sum: '<S1>/Sum1'
   */
  uSz_tmp = ((((3.3333 * rtU.In1 + -4.5807 * rtDW.Tz_states[0]) + 1.6225 *
               rtDW.Tz_states[1]) - ((3.0 * rtU.In2 + -3.939 * rtDW.Rz_states[0])
    + 1.3142 * rtDW.Rz_states[1])) - -0.3742 * rtDW.uSz_states[0]) - -0.6258 *
    rtDW.uSz_states[1];

  /* Outport: '<Root>/Out1' incorporates:
   *  DiscreteFilter: '<S1>/1//S(z)'
   */
  rtY.Out1 = uSz_tmp;

  /* Update for DiscreteFilter: '<S1>/T(z)' incorporates:
   *  Inport: '<Root>/In1'
   */
  rtDW.Tz_states[1] = rtDW.Tz_states[0];
  rtDW.Tz_states[0] = rtU.In1;

  /* Update for DiscreteFilter: '<S1>/R(z)' incorporates:
   *  Inport: '<Root>/In2'
   */
  rtDW.Rz_states[1] = rtDW.Rz_states[0];
  rtDW.Rz_states[0] = rtU.In2;

  /* Update for DiscreteFilter: '<S1>/1//S(z)' */
  rtDW.uSz_states[1] = rtDW.uSz_states[0];
  rtDW.uSz_states[0] = uSz_tmp;
}

/* Model initialize function */
void Subsystem_initialize(void)
{
  /* (no initialization code required) */
}

/*
 * File trailer for generated code.
 *
 * [EOF]
 */
