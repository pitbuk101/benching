// Generated from io/wren/base/type/parser/antlr/v4/PgNumericFormat.g4 by ANTLR 4.13.2
package io.wren.base.type.parser.antlr.v4;
import org.antlr.v4.runtime.tree.ParseTreeListener;

/**
 * This interface defines a complete listener for a parse tree produced by
 * {@link PgNumericFormatParser}.
 */
public interface PgNumericFormatListener extends ParseTreeListener {
	/**
	 * Enter a parse tree produced by {@link PgNumericFormatParser#format}.
	 * @param ctx the parse tree
	 */
	void enterFormat(PgNumericFormatParser.FormatContext ctx);
	/**
	 * Exit a parse tree produced by {@link PgNumericFormatParser#format}.
	 * @param ctx the parse tree
	 */
	void exitFormat(PgNumericFormatParser.FormatContext ctx);
	/**
	 * Enter a parse tree produced by the {@code digitPattern}
	 * labeled alternative in {@link PgNumericFormatParser#pattern}.
	 * @param ctx the parse tree
	 */
	void enterDigitPattern(PgNumericFormatParser.DigitPatternContext ctx);
	/**
	 * Exit a parse tree produced by the {@code digitPattern}
	 * labeled alternative in {@link PgNumericFormatParser#pattern}.
	 * @param ctx the parse tree
	 */
	void exitDigitPattern(PgNumericFormatParser.DigitPatternContext ctx);
	/**
	 * Enter a parse tree produced by the {@code decimalPointPattern}
	 * labeled alternative in {@link PgNumericFormatParser#pattern}.
	 * @param ctx the parse tree
	 */
	void enterDecimalPointPattern(PgNumericFormatParser.DecimalPointPatternContext ctx);
	/**
	 * Exit a parse tree produced by the {@code decimalPointPattern}
	 * labeled alternative in {@link PgNumericFormatParser#pattern}.
	 * @param ctx the parse tree
	 */
	void exitDecimalPointPattern(PgNumericFormatParser.DecimalPointPatternContext ctx);
	/**
	 * Enter a parse tree produced by the {@code groupSeparatorPattern}
	 * labeled alternative in {@link PgNumericFormatParser#pattern}.
	 * @param ctx the parse tree
	 */
	void enterGroupSeparatorPattern(PgNumericFormatParser.GroupSeparatorPatternContext ctx);
	/**
	 * Exit a parse tree produced by the {@code groupSeparatorPattern}
	 * labeled alternative in {@link PgNumericFormatParser#pattern}.
	 * @param ctx the parse tree
	 */
	void exitGroupSeparatorPattern(PgNumericFormatParser.GroupSeparatorPatternContext ctx);
	/**
	 * Enter a parse tree produced by the {@code currencySymbolPattern}
	 * labeled alternative in {@link PgNumericFormatParser#pattern}.
	 * @param ctx the parse tree
	 */
	void enterCurrencySymbolPattern(PgNumericFormatParser.CurrencySymbolPatternContext ctx);
	/**
	 * Exit a parse tree produced by the {@code currencySymbolPattern}
	 * labeled alternative in {@link PgNumericFormatParser#pattern}.
	 * @param ctx the parse tree
	 */
	void exitCurrencySymbolPattern(PgNumericFormatParser.CurrencySymbolPatternContext ctx);
	/**
	 * Enter a parse tree produced by the {@code exponentPattern}
	 * labeled alternative in {@link PgNumericFormatParser#pattern}.
	 * @param ctx the parse tree
	 */
	void enterExponentPattern(PgNumericFormatParser.ExponentPatternContext ctx);
	/**
	 * Exit a parse tree produced by the {@code exponentPattern}
	 * labeled alternative in {@link PgNumericFormatParser#pattern}.
	 * @param ctx the parse tree
	 */
	void exitExponentPattern(PgNumericFormatParser.ExponentPatternContext ctx);
	/**
	 * Enter a parse tree produced by the {@code nonReservedPattern}
	 * labeled alternative in {@link PgNumericFormatParser#pattern}.
	 * @param ctx the parse tree
	 */
	void enterNonReservedPattern(PgNumericFormatParser.NonReservedPatternContext ctx);
	/**
	 * Exit a parse tree produced by the {@code nonReservedPattern}
	 * labeled alternative in {@link PgNumericFormatParser#pattern}.
	 * @param ctx the parse tree
	 */
	void exitNonReservedPattern(PgNumericFormatParser.NonReservedPatternContext ctx);
	/**
	 * Enter a parse tree produced by {@link PgNumericFormatParser#nonReserved}.
	 * @param ctx the parse tree
	 */
	void enterNonReserved(PgNumericFormatParser.NonReservedContext ctx);
	/**
	 * Exit a parse tree produced by {@link PgNumericFormatParser#nonReserved}.
	 * @param ctx the parse tree
	 */
	void exitNonReserved(PgNumericFormatParser.NonReservedContext ctx);
}