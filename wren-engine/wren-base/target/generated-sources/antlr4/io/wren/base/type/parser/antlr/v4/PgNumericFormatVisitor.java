// Generated from io/wren/base/type/parser/antlr/v4/PgNumericFormat.g4 by ANTLR 4.13.2
package io.wren.base.type.parser.antlr.v4;
import org.antlr.v4.runtime.tree.ParseTreeVisitor;

/**
 * This interface defines a complete generic visitor for a parse tree produced
 * by {@link PgNumericFormatParser}.
 *
 * @param <T> The return type of the visit operation. Use {@link Void} for
 * operations with no return type.
 */
public interface PgNumericFormatVisitor<T> extends ParseTreeVisitor<T> {
	/**
	 * Visit a parse tree produced by {@link PgNumericFormatParser#format}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitFormat(PgNumericFormatParser.FormatContext ctx);
	/**
	 * Visit a parse tree produced by the {@code digitPattern}
	 * labeled alternative in {@link PgNumericFormatParser#pattern}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitDigitPattern(PgNumericFormatParser.DigitPatternContext ctx);
	/**
	 * Visit a parse tree produced by the {@code decimalPointPattern}
	 * labeled alternative in {@link PgNumericFormatParser#pattern}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitDecimalPointPattern(PgNumericFormatParser.DecimalPointPatternContext ctx);
	/**
	 * Visit a parse tree produced by the {@code groupSeparatorPattern}
	 * labeled alternative in {@link PgNumericFormatParser#pattern}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitGroupSeparatorPattern(PgNumericFormatParser.GroupSeparatorPatternContext ctx);
	/**
	 * Visit a parse tree produced by the {@code currencySymbolPattern}
	 * labeled alternative in {@link PgNumericFormatParser#pattern}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitCurrencySymbolPattern(PgNumericFormatParser.CurrencySymbolPatternContext ctx);
	/**
	 * Visit a parse tree produced by the {@code exponentPattern}
	 * labeled alternative in {@link PgNumericFormatParser#pattern}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitExponentPattern(PgNumericFormatParser.ExponentPatternContext ctx);
	/**
	 * Visit a parse tree produced by the {@code nonReservedPattern}
	 * labeled alternative in {@link PgNumericFormatParser#pattern}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitNonReservedPattern(PgNumericFormatParser.NonReservedPatternContext ctx);
	/**
	 * Visit a parse tree produced by {@link PgNumericFormatParser#nonReserved}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitNonReserved(PgNumericFormatParser.NonReservedContext ctx);
}