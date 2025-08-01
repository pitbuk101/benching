// Generated from io/wren/base/type/parser/antlr/v4/PgDateTimeFormat.g4 by ANTLR 4.13.2
package io.wren.base.type.parser.antlr.v4;
import org.antlr.v4.runtime.tree.ParseTreeVisitor;

/**
 * This interface defines a complete generic visitor for a parse tree produced
 * by {@link PgDateTimeFormatParser}.
 *
 * @param <T> The return type of the visit operation. Use {@link Void} for
 * operations with no return type.
 */
public interface PgDateTimeFormatVisitor<T> extends ParseTreeVisitor<T> {
	/**
	 * Visit a parse tree produced by {@link PgDateTimeFormatParser#format}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitFormat(PgDateTimeFormatParser.FormatContext ctx);
	/**
	 * Visit a parse tree produced by {@link PgDateTimeFormatParser#symbol}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitSymbol(PgDateTimeFormatParser.SymbolContext ctx);
	/**
	 * Visit a parse tree produced by the {@code hourLiteral}
	 * labeled alternative in {@link PgDateTimeFormatParser#pattern}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitHourLiteral(PgDateTimeFormatParser.HourLiteralContext ctx);
	/**
	 * Visit a parse tree produced by the {@code minuteLiteral}
	 * labeled alternative in {@link PgDateTimeFormatParser#pattern}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitMinuteLiteral(PgDateTimeFormatParser.MinuteLiteralContext ctx);
	/**
	 * Visit a parse tree produced by the {@code secondLiteral}
	 * labeled alternative in {@link PgDateTimeFormatParser#pattern}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitSecondLiteral(PgDateTimeFormatParser.SecondLiteralContext ctx);
	/**
	 * Visit a parse tree produced by the {@code milliSecondLiteral}
	 * labeled alternative in {@link PgDateTimeFormatParser#pattern}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitMilliSecondLiteral(PgDateTimeFormatParser.MilliSecondLiteralContext ctx);
	/**
	 * Visit a parse tree produced by the {@code yearLiteral}
	 * labeled alternative in {@link PgDateTimeFormatParser#pattern}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitYearLiteral(PgDateTimeFormatParser.YearLiteralContext ctx);
	/**
	 * Visit a parse tree produced by the {@code monthLiteral}
	 * labeled alternative in {@link PgDateTimeFormatParser#pattern}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitMonthLiteral(PgDateTimeFormatParser.MonthLiteralContext ctx);
	/**
	 * Visit a parse tree produced by the {@code dayLiteral}
	 * labeled alternative in {@link PgDateTimeFormatParser#pattern}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitDayLiteral(PgDateTimeFormatParser.DayLiteralContext ctx);
	/**
	 * Visit a parse tree produced by the {@code weekLiteral}
	 * labeled alternative in {@link PgDateTimeFormatParser#pattern}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitWeekLiteral(PgDateTimeFormatParser.WeekLiteralContext ctx);
	/**
	 * Visit a parse tree produced by the {@code timeZoneLiteral}
	 * labeled alternative in {@link PgDateTimeFormatParser#pattern}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitTimeZoneLiteral(PgDateTimeFormatParser.TimeZoneLiteralContext ctx);
	/**
	 * Visit a parse tree produced by the {@code meridiemMarkerLiteral}
	 * labeled alternative in {@link PgDateTimeFormatParser#pattern}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitMeridiemMarkerLiteral(PgDateTimeFormatParser.MeridiemMarkerLiteralContext ctx);
	/**
	 * Visit a parse tree produced by the {@code eraDesignatorLiteral}
	 * labeled alternative in {@link PgDateTimeFormatParser#pattern}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitEraDesignatorLiteral(PgDateTimeFormatParser.EraDesignatorLiteralContext ctx);
	/**
	 * Visit a parse tree produced by {@link PgDateTimeFormatParser#separator}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitSeparator(PgDateTimeFormatParser.SeparatorContext ctx);
}