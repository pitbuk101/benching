// Generated from io/wren/base/type/parser/antlr/v4/PgDateTimeFormat.g4 by ANTLR 4.13.2
package io.wren.base.type.parser.antlr.v4;
import org.antlr.v4.runtime.tree.ParseTreeListener;

/**
 * This interface defines a complete listener for a parse tree produced by
 * {@link PgDateTimeFormatParser}.
 */
public interface PgDateTimeFormatListener extends ParseTreeListener {
	/**
	 * Enter a parse tree produced by {@link PgDateTimeFormatParser#format}.
	 * @param ctx the parse tree
	 */
	void enterFormat(PgDateTimeFormatParser.FormatContext ctx);
	/**
	 * Exit a parse tree produced by {@link PgDateTimeFormatParser#format}.
	 * @param ctx the parse tree
	 */
	void exitFormat(PgDateTimeFormatParser.FormatContext ctx);
	/**
	 * Enter a parse tree produced by {@link PgDateTimeFormatParser#symbol}.
	 * @param ctx the parse tree
	 */
	void enterSymbol(PgDateTimeFormatParser.SymbolContext ctx);
	/**
	 * Exit a parse tree produced by {@link PgDateTimeFormatParser#symbol}.
	 * @param ctx the parse tree
	 */
	void exitSymbol(PgDateTimeFormatParser.SymbolContext ctx);
	/**
	 * Enter a parse tree produced by the {@code hourLiteral}
	 * labeled alternative in {@link PgDateTimeFormatParser#pattern}.
	 * @param ctx the parse tree
	 */
	void enterHourLiteral(PgDateTimeFormatParser.HourLiteralContext ctx);
	/**
	 * Exit a parse tree produced by the {@code hourLiteral}
	 * labeled alternative in {@link PgDateTimeFormatParser#pattern}.
	 * @param ctx the parse tree
	 */
	void exitHourLiteral(PgDateTimeFormatParser.HourLiteralContext ctx);
	/**
	 * Enter a parse tree produced by the {@code minuteLiteral}
	 * labeled alternative in {@link PgDateTimeFormatParser#pattern}.
	 * @param ctx the parse tree
	 */
	void enterMinuteLiteral(PgDateTimeFormatParser.MinuteLiteralContext ctx);
	/**
	 * Exit a parse tree produced by the {@code minuteLiteral}
	 * labeled alternative in {@link PgDateTimeFormatParser#pattern}.
	 * @param ctx the parse tree
	 */
	void exitMinuteLiteral(PgDateTimeFormatParser.MinuteLiteralContext ctx);
	/**
	 * Enter a parse tree produced by the {@code secondLiteral}
	 * labeled alternative in {@link PgDateTimeFormatParser#pattern}.
	 * @param ctx the parse tree
	 */
	void enterSecondLiteral(PgDateTimeFormatParser.SecondLiteralContext ctx);
	/**
	 * Exit a parse tree produced by the {@code secondLiteral}
	 * labeled alternative in {@link PgDateTimeFormatParser#pattern}.
	 * @param ctx the parse tree
	 */
	void exitSecondLiteral(PgDateTimeFormatParser.SecondLiteralContext ctx);
	/**
	 * Enter a parse tree produced by the {@code milliSecondLiteral}
	 * labeled alternative in {@link PgDateTimeFormatParser#pattern}.
	 * @param ctx the parse tree
	 */
	void enterMilliSecondLiteral(PgDateTimeFormatParser.MilliSecondLiteralContext ctx);
	/**
	 * Exit a parse tree produced by the {@code milliSecondLiteral}
	 * labeled alternative in {@link PgDateTimeFormatParser#pattern}.
	 * @param ctx the parse tree
	 */
	void exitMilliSecondLiteral(PgDateTimeFormatParser.MilliSecondLiteralContext ctx);
	/**
	 * Enter a parse tree produced by the {@code yearLiteral}
	 * labeled alternative in {@link PgDateTimeFormatParser#pattern}.
	 * @param ctx the parse tree
	 */
	void enterYearLiteral(PgDateTimeFormatParser.YearLiteralContext ctx);
	/**
	 * Exit a parse tree produced by the {@code yearLiteral}
	 * labeled alternative in {@link PgDateTimeFormatParser#pattern}.
	 * @param ctx the parse tree
	 */
	void exitYearLiteral(PgDateTimeFormatParser.YearLiteralContext ctx);
	/**
	 * Enter a parse tree produced by the {@code monthLiteral}
	 * labeled alternative in {@link PgDateTimeFormatParser#pattern}.
	 * @param ctx the parse tree
	 */
	void enterMonthLiteral(PgDateTimeFormatParser.MonthLiteralContext ctx);
	/**
	 * Exit a parse tree produced by the {@code monthLiteral}
	 * labeled alternative in {@link PgDateTimeFormatParser#pattern}.
	 * @param ctx the parse tree
	 */
	void exitMonthLiteral(PgDateTimeFormatParser.MonthLiteralContext ctx);
	/**
	 * Enter a parse tree produced by the {@code dayLiteral}
	 * labeled alternative in {@link PgDateTimeFormatParser#pattern}.
	 * @param ctx the parse tree
	 */
	void enterDayLiteral(PgDateTimeFormatParser.DayLiteralContext ctx);
	/**
	 * Exit a parse tree produced by the {@code dayLiteral}
	 * labeled alternative in {@link PgDateTimeFormatParser#pattern}.
	 * @param ctx the parse tree
	 */
	void exitDayLiteral(PgDateTimeFormatParser.DayLiteralContext ctx);
	/**
	 * Enter a parse tree produced by the {@code weekLiteral}
	 * labeled alternative in {@link PgDateTimeFormatParser#pattern}.
	 * @param ctx the parse tree
	 */
	void enterWeekLiteral(PgDateTimeFormatParser.WeekLiteralContext ctx);
	/**
	 * Exit a parse tree produced by the {@code weekLiteral}
	 * labeled alternative in {@link PgDateTimeFormatParser#pattern}.
	 * @param ctx the parse tree
	 */
	void exitWeekLiteral(PgDateTimeFormatParser.WeekLiteralContext ctx);
	/**
	 * Enter a parse tree produced by the {@code timeZoneLiteral}
	 * labeled alternative in {@link PgDateTimeFormatParser#pattern}.
	 * @param ctx the parse tree
	 */
	void enterTimeZoneLiteral(PgDateTimeFormatParser.TimeZoneLiteralContext ctx);
	/**
	 * Exit a parse tree produced by the {@code timeZoneLiteral}
	 * labeled alternative in {@link PgDateTimeFormatParser#pattern}.
	 * @param ctx the parse tree
	 */
	void exitTimeZoneLiteral(PgDateTimeFormatParser.TimeZoneLiteralContext ctx);
	/**
	 * Enter a parse tree produced by the {@code meridiemMarkerLiteral}
	 * labeled alternative in {@link PgDateTimeFormatParser#pattern}.
	 * @param ctx the parse tree
	 */
	void enterMeridiemMarkerLiteral(PgDateTimeFormatParser.MeridiemMarkerLiteralContext ctx);
	/**
	 * Exit a parse tree produced by the {@code meridiemMarkerLiteral}
	 * labeled alternative in {@link PgDateTimeFormatParser#pattern}.
	 * @param ctx the parse tree
	 */
	void exitMeridiemMarkerLiteral(PgDateTimeFormatParser.MeridiemMarkerLiteralContext ctx);
	/**
	 * Enter a parse tree produced by the {@code eraDesignatorLiteral}
	 * labeled alternative in {@link PgDateTimeFormatParser#pattern}.
	 * @param ctx the parse tree
	 */
	void enterEraDesignatorLiteral(PgDateTimeFormatParser.EraDesignatorLiteralContext ctx);
	/**
	 * Exit a parse tree produced by the {@code eraDesignatorLiteral}
	 * labeled alternative in {@link PgDateTimeFormatParser#pattern}.
	 * @param ctx the parse tree
	 */
	void exitEraDesignatorLiteral(PgDateTimeFormatParser.EraDesignatorLiteralContext ctx);
	/**
	 * Enter a parse tree produced by {@link PgDateTimeFormatParser#separator}.
	 * @param ctx the parse tree
	 */
	void enterSeparator(PgDateTimeFormatParser.SeparatorContext ctx);
	/**
	 * Exit a parse tree produced by {@link PgDateTimeFormatParser#separator}.
	 * @param ctx the parse tree
	 */
	void exitSeparator(PgDateTimeFormatParser.SeparatorContext ctx);
}