// Generated from io/wren/base/macro/ParameterListBase.g4 by ANTLR 4.13.2
package io.wren.base.macro;
import org.antlr.v4.runtime.tree.ParseTreeListener;

/**
 * This interface defines a complete listener for a parse tree produced by
 * {@link ParameterListBaseParser}.
 */
public interface ParameterListBaseListener extends ParseTreeListener {
	/**
	 * Enter a parse tree produced by {@link ParameterListBaseParser#parameterList}.
	 * @param ctx the parse tree
	 */
	void enterParameterList(ParameterListBaseParser.ParameterListContext ctx);
	/**
	 * Exit a parse tree produced by {@link ParameterListBaseParser#parameterList}.
	 * @param ctx the parse tree
	 */
	void exitParameterList(ParameterListBaseParser.ParameterListContext ctx);
	/**
	 * Enter a parse tree produced by {@link ParameterListBaseParser#parameter}.
	 * @param ctx the parse tree
	 */
	void enterParameter(ParameterListBaseParser.ParameterContext ctx);
	/**
	 * Exit a parse tree produced by {@link ParameterListBaseParser#parameter}.
	 * @param ctx the parse tree
	 */
	void exitParameter(ParameterListBaseParser.ParameterContext ctx);
	/**
	 * Enter a parse tree produced by {@link ParameterListBaseParser#typeName}.
	 * @param ctx the parse tree
	 */
	void enterTypeName(ParameterListBaseParser.TypeNameContext ctx);
	/**
	 * Exit a parse tree produced by {@link ParameterListBaseParser#typeName}.
	 * @param ctx the parse tree
	 */
	void exitTypeName(ParameterListBaseParser.TypeNameContext ctx);
	/**
	 * Enter a parse tree produced by {@link ParameterListBaseParser#paraName}.
	 * @param ctx the parse tree
	 */
	void enterParaName(ParameterListBaseParser.ParaNameContext ctx);
	/**
	 * Exit a parse tree produced by {@link ParameterListBaseParser#paraName}.
	 * @param ctx the parse tree
	 */
	void exitParaName(ParameterListBaseParser.ParaNameContext ctx);
}