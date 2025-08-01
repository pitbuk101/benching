// Generated from io/wren/base/type/parser/antlr/v4/PgArray.g4 by ANTLR 4.13.2
package io.wren.base.type.parser.antlr.v4;
import org.antlr.v4.runtime.tree.ParseTreeListener;

/**
 * This interface defines a complete listener for a parse tree produced by
 * {@link PgArrayParser}.
 */
public interface PgArrayListener extends ParseTreeListener {
	/**
	 * Enter a parse tree produced by {@link PgArrayParser#array}.
	 * @param ctx the parse tree
	 */
	void enterArray(PgArrayParser.ArrayContext ctx);
	/**
	 * Exit a parse tree produced by {@link PgArrayParser#array}.
	 * @param ctx the parse tree
	 */
	void exitArray(PgArrayParser.ArrayContext ctx);
	/**
	 * Enter a parse tree produced by {@link PgArrayParser#item}.
	 * @param ctx the parse tree
	 */
	void enterItem(PgArrayParser.ItemContext ctx);
	/**
	 * Exit a parse tree produced by {@link PgArrayParser#item}.
	 * @param ctx the parse tree
	 */
	void exitItem(PgArrayParser.ItemContext ctx);
	/**
	 * Enter a parse tree produced by the {@code quotedString}
	 * labeled alternative in {@link PgArrayParser#string}.
	 * @param ctx the parse tree
	 */
	void enterQuotedString(PgArrayParser.QuotedStringContext ctx);
	/**
	 * Exit a parse tree produced by the {@code quotedString}
	 * labeled alternative in {@link PgArrayParser#string}.
	 * @param ctx the parse tree
	 */
	void exitQuotedString(PgArrayParser.QuotedStringContext ctx);
	/**
	 * Enter a parse tree produced by the {@code null}
	 * labeled alternative in {@link PgArrayParser#string}.
	 * @param ctx the parse tree
	 */
	void enterNull(PgArrayParser.NullContext ctx);
	/**
	 * Exit a parse tree produced by the {@code null}
	 * labeled alternative in {@link PgArrayParser#string}.
	 * @param ctx the parse tree
	 */
	void exitNull(PgArrayParser.NullContext ctx);
	/**
	 * Enter a parse tree produced by the {@code unquotedString}
	 * labeled alternative in {@link PgArrayParser#string}.
	 * @param ctx the parse tree
	 */
	void enterUnquotedString(PgArrayParser.UnquotedStringContext ctx);
	/**
	 * Exit a parse tree produced by the {@code unquotedString}
	 * labeled alternative in {@link PgArrayParser#string}.
	 * @param ctx the parse tree
	 */
	void exitUnquotedString(PgArrayParser.UnquotedStringContext ctx);
}