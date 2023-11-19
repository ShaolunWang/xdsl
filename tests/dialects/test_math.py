from typing import TypeVar
import pytest
from xdsl.ir import (
    Attribute,
    Dialect,
    Operation,
    OpResult,
    ParametrizedAttribute,
    SSAValue,
    TypeAttribute,
)
from xdsl.irdl import (
    IRDLOperation,
    Operand,
    OptOperand,
    OptOpResult,
    ParameterDef,
    attr_def,
    irdl_attr_definition,
    irdl_op_definition,
    operand_def,
    opt_attr_def,
    opt_operand_def,
    opt_result_def,
    result_def,
)
from xdsl.irdl import OperandDef
from xdsl.dialects.arith import BinaryOperation, CeilDivSI, Constant, TruncFOp
from xdsl.dialects.builtin import AnyFloatAttr, FloatAttr,  f32, AnyFloat, i32, Float32Type
from xdsl.dialects.experimental.math import (
        AbsFOp,
        AbsIOp,
        Atan2Op,
        AtanOp,
        CbrtOp,
        CeilOp,
        CopySignOp,
        CosOp,
        CountLeadingZerosOp,
        CountTrailingZerosOp,
        CtPopOp,
        ErfOp,
        Exp2Op,
        ExpM1Op,
        ExpOp,
        FPowIOp,
        FloorOp,
        FmaOp,
        IPowIOp,
        Log10Op,
        Log1pOp,
        Log2Op,
        LogOp,
        PowFOp,
        RoundEvenOp,
        RoundOp,
        RsqrtOp,
        SinOp,
        SqrtOp,
        TanOp,
        TanhOp,
        TruncOp,
)

from xdsl.dialects.builtin import f32

from xdsl.ir import Attribute
#from xdsl.utils.exceptions import VerifyException

_BinOpArgT = TypeVar("_BinOpArgT", bound=Attribute)
class Test_float_math_binary_construction:
    operand_type = f32
    a = Constant(FloatAttr(1.1, operand_type))
    b = Constant(FloatAttr(2.2, operand_type))
    @pytest.mark.parametrize(
        "OpClass",
        [
            Atan2Op,
            CopySignOp,
            IPowIOp,
            PowFOp,
        ]
    )
    @pytest.mark.parametrize('return_type', [None, operand_type])

    def test_float_binary_math_ops_init(self,
                           OpClass: type[BinaryOperation[_BinOpArgT]], return_type: Attribute,
                           ):
        op = OpClass(self.a, self.b)
        assert isinstance(op, OpClass)
        assert op.lhs.owner is self.a
        assert op.rhs.owner is self.b
        assert op.result.type == self.operand_type
        
class Test_float_math_unary_constructions:
    operand_type = f32
    a = Constant(FloatAttr(1, operand_type))
    @pytest.mark.parametrize(
        "OpClass",
        [
            AbsFOp,
            AtanOp,
            CbrtOp,
            CeilOp,
            CosOp,
            ErfOp,
            Exp2Op,
            ExpM1Op,
            ExpOp,
            FloorOp,
            Log10Op,
            Log1pOp,
            Log2Op,
            LogOp,
            RoundEvenOp,
            RoundOp,
            RsqrtOp,
            SinOp,
            SqrtOp,
            TanOp,
            TanhOp,
            TruncOp,
        ]
    )
    @pytest.mark.parametrize('return_type', [operand_type])
    def test_float_math_ops_init(self,
                           OpClass: type, return_type: Attribute, # FIXME
                           ):
        op = OpClass(self.a)
        assert op.result.type == f32
        assert op.operand.type == f32
        assert op.operand.owner == self.a
        assert op.result.type == self.operand_type
class Test_int_math_unary_constructions:
    operand_type = i32
    a = Constant.from_int_and_width(0, 32)
    @pytest.mark.parametrize(
        "OpClass",
        [
            AbsIOp,
            CountLeadingZerosOp,
            CountTrailingZerosOp,
            CtPopOp,
        ]
    )
    @pytest.mark.parametrize('return_type', [operand_type])
    def test_int_math_ops_init(self,
                           OpClass: type, return_type: Attribute, # FIXME use something other than `type`
                           ):
        op = OpClass(self.a)
        assert op.result.type == i32
        assert op.operand.type == i32
        assert op.operand.owner == self.a
        assert op.result.type == self.operand_type

class Test_fpowi:
    a = Constant(FloatAttr(2.2, f32))
    b = Constant.from_int_and_width(0, 32)

    def test_fpowi_construction(self):
        op = FPowIOp(self.a, self.b)
        assert op.result.type == f32
        assert op.lhs.owner is self.a
        assert op.rhs.owner is self.b
        assert op.result.type == f32

class Test_fma:
    a = Constant(FloatAttr(1.1, f32))
    b = Constant(FloatAttr(2.2, f32))
    c = Constant(FloatAttr(3.3, f32))
    
    def test_fma_construction(self):

        op = FmaOp(self.a, self.b, self.c)
        assert op.result.type == f32
        assert op.a.owner is self.a
        assert op.b.owner is self.b
        assert op.c.owner is self.c
        assert op.result.type == f32
