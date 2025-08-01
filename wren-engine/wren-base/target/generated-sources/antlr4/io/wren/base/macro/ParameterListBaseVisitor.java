// Generated from io/wren/base/macro/ParameterListBase.g4 by ANTLR 4.13.2
package io.wren.base.macro;
import org.antlr.v4.runtime.tree.ParseTreeVisitor;

/**
 * This interface defines a complete generic visitor for a parse tree produced
 * by {@link ParameterListBaseParser}.
 *
 * @param <T> The return type of the visit operation. Use {@link Void} for
 * operations with no return type.
 */
public interface ParameterListBaseVisitor<T> extends ParseTreeVisitor<T> {
	/**
	 * Visit a parse tree produced by {@link ParameterListBaseParser#parameterList}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitParameterList(ParameterListBaseParser.ParameterListContext ctx);
	/**
	 * Visit a parse tree produced by {@link ParameterListBaseParser#parameter}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitParameter(ParameterListBaseParser.ParameterContext ctx);
	/**
	 * Visit a parse tree produced by {@link ParameterListBaseParser#typeName}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitTypeName(ParameterListBaseParser.TypeNameContext ctx);
	/**
	 * Visit a parse tree produced by {@link ParameterListBaseParser#paraName}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitParaName(ParameterListBaseParser.ParaNameContext ctx);
}