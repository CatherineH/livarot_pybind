#ifndef INKSCAPE_LIVAROT_BOOL_OP_H
#define INKSCAPE_LIVAROT_BOOL_OP_H

// boolean operation
enum bool_op
{
  bool_op_union,		// A OR B
  bool_op_inters,		// A AND B
  bool_op_diff,			// A \ B
  bool_op_symdiff,  // A XOR B
  bool_op_cut,      // coupure (pleines)
  bool_op_slice     // coupure (contour)
};
typedef enum bool_op BooleanOp;

#endif