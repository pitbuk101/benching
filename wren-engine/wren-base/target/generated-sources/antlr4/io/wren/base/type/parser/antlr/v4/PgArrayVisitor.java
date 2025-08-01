// Generated from io/wren/base/type/parser/antlr/v4/PgArray.g4 by ANTLR 4.13.2
package io.wren.base.type.parser.antlr.v4;
import org.antlr.v4.runtime.tree.ParseTreeVisitor;

/**
 * This interface defines a complete generic visitor for a parse tree produced
 * by {@link PgArrayParser}.
 *
 * @param <T> The return type of the visit operation. Use {@link Void} for
 * operations with no return type.
 */
public interface PgArrayVisitor<T> extends ParseTreeVisitor<T> {
	/**
	 * Visit a parse tree produced by {@link PgArrayParser#array}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitArray(PgArrayParser.ArrayContext ctx);
	/**
	 * Visit a parse tree produced by {@link PgArrayParser#item}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitItem(PgArrayParser.ItemContext ctx);
	/**
	 * Visit a parse tree produced by the {@code quotedString}
	 * labeled alternative in {@link PgArrayParser#string}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitQuotedString(PgArrayParser.QuotedStringContext ctx);
	/**
	 * Visit a parse tree produced by the {@code null}
	 * labeled alternative in {@link PgArrayParser#string}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitNull(PgArrayParser.NullContext ctx);
	/**
	 * Visit a parse tree produced by the {@code unquotedString}
	 * labeled alternative in {@link PgArrayParser#string}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitUnquotedString(PgArrayParser.UnquotedStringContext ctx);
}