// Generated from io/wren/base/type/parser/antlr/v4/PgNumericFormat.g4 by ANTLR 4.13.2
package io.wren.base.type.parser.antlr.v4;
import org.antlr.v4.runtime.atn.*;
import org.antlr.v4.runtime.dfa.DFA;
import org.antlr.v4.runtime.*;
import org.antlr.v4.runtime.misc.*;
import org.antlr.v4.runtime.tree.*;
import java.util.List;
import java.util.Iterator;
import java.util.ArrayList;

@SuppressWarnings({"all", "warnings", "unchecked", "unused", "cast", "CheckReturnValue", "this-escape"})
public class PgNumericFormatParser extends Parser {
	static { RuntimeMetaData.checkVersion("4.13.2", RuntimeMetaData.VERSION); }

	protected static final DFA[] _decisionToDFA;
	protected static final PredictionContextCache _sharedContextCache =
		new PredictionContextCache();
	public static final int
		DIGIT_CAN_DROP=1, DIGIT_CAN_NOT_DROP=2, DECIMAL_POINT=3, GROUP_SEPARATOR=4, 
		PR=5, SIGN_ANCHOR_LOCALE=6, CURRENCY_SYMBOL=7, DECIMAL_POINT_LOCALE=8, 
		GROUP_SEPARATOR_LOCALE=9, MINUS=10, PLUS=11, SIGN=12, ROMAN=13, ORDINAL=14, 
		SHIFT_DIGIT=15, EXPONENT=16, FM=17;
	public static final int
		RULE_format = 0, RULE_pattern = 1, RULE_nonReserved = 2;
	private static String[] makeRuleNames() {
		return new String[] {
			"format", "pattern", "nonReserved"
		};
	}
	public static final String[] ruleNames = makeRuleNames();

	private static String[] makeLiteralNames() {
		return new String[] {
			null, "'9'", "'0'", "'.'", "','", "'PR'", "'S'", "'L'", "'D'", "'G'", 
			"'MI'", "'PL'", "'SG'", "'RN'", null, "'V'", "'EEEE'", "'FM'"
		};
	}
	private static final String[] _LITERAL_NAMES = makeLiteralNames();
	private static String[] makeSymbolicNames() {
		return new String[] {
			null, "DIGIT_CAN_DROP", "DIGIT_CAN_NOT_DROP", "DECIMAL_POINT", "GROUP_SEPARATOR", 
			"PR", "SIGN_ANCHOR_LOCALE", "CURRENCY_SYMBOL", "DECIMAL_POINT_LOCALE", 
			"GROUP_SEPARATOR_LOCALE", "MINUS", "PLUS", "SIGN", "ROMAN", "ORDINAL", 
			"SHIFT_DIGIT", "EXPONENT", "FM"
		};
	}
	private static final String[] _SYMBOLIC_NAMES = makeSymbolicNames();
	public static final Vocabulary VOCABULARY = new VocabularyImpl(_LITERAL_NAMES, _SYMBOLIC_NAMES);

	/**
	 * @deprecated Use {@link #VOCABULARY} instead.
	 */
	@Deprecated
	public static final String[] tokenNames;
	static {
		tokenNames = new String[_SYMBOLIC_NAMES.length];
		for (int i = 0; i < tokenNames.length; i++) {
			tokenNames[i] = VOCABULARY.getLiteralName(i);
			if (tokenNames[i] == null) {
				tokenNames[i] = VOCABULARY.getSymbolicName(i);
			}

			if (tokenNames[i] == null) {
				tokenNames[i] = "<INVALID>";
			}
		}
	}

	@Override
	@Deprecated
	public String[] getTokenNames() {
		return tokenNames;
	}

	@Override

	public Vocabulary getVocabulary() {
		return VOCABULARY;
	}

	@Override
	public String getGrammarFileName() { return "PgNumericFormat.g4"; }

	@Override
	public String[] getRuleNames() { return ruleNames; }

	@Override
	public String getSerializedATN() { return _serializedATN; }

	@Override
	public ATN getATN() { return _ATN; }

	public PgNumericFormatParser(TokenStream input) {
		super(input);
		_interp = new ParserATNSimulator(this,_ATN,_decisionToDFA,_sharedContextCache);
	}

	@SuppressWarnings("CheckReturnValue")
	public static class FormatContext extends ParserRuleContext {
		public List<PatternContext> pattern() {
			return getRuleContexts(PatternContext.class);
		}
		public PatternContext pattern(int i) {
			return getRuleContext(PatternContext.class,i);
		}
		public FormatContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_format; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof PgNumericFormatListener ) ((PgNumericFormatListener)listener).enterFormat(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof PgNumericFormatListener ) ((PgNumericFormatListener)listener).exitFormat(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof PgNumericFormatVisitor ) return ((PgNumericFormatVisitor<? extends T>)visitor).visitFormat(this);
			else return visitor.visitChildren(this);
		}
	}

	public final FormatContext format() throws RecognitionException {
		FormatContext _localctx = new FormatContext(_ctx, getState());
		enterRule(_localctx, 0, RULE_format);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(6);
			pattern();
			setState(10);
			_errHandler.sync(this);
			_la = _input.LA(1);
			while ((((_la) & ~0x3f) == 0 && ((1L << _la) & 262142L) != 0)) {
				{
				{
				setState(7);
				pattern();
				}
				}
				setState(12);
				_errHandler.sync(this);
				_la = _input.LA(1);
			}
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class PatternContext extends ParserRuleContext {
		public PatternContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_pattern; }
	 
		public PatternContext() { }
		public void copyFrom(PatternContext ctx) {
			super.copyFrom(ctx);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class ExponentPatternContext extends PatternContext {
		public TerminalNode EXPONENT() { return getToken(PgNumericFormatParser.EXPONENT, 0); }
		public ExponentPatternContext(PatternContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof PgNumericFormatListener ) ((PgNumericFormatListener)listener).enterExponentPattern(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof PgNumericFormatListener ) ((PgNumericFormatListener)listener).exitExponentPattern(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof PgNumericFormatVisitor ) return ((PgNumericFormatVisitor<? extends T>)visitor).visitExponentPattern(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class CurrencySymbolPatternContext extends PatternContext {
		public TerminalNode CURRENCY_SYMBOL() { return getToken(PgNumericFormatParser.CURRENCY_SYMBOL, 0); }
		public CurrencySymbolPatternContext(PatternContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof PgNumericFormatListener ) ((PgNumericFormatListener)listener).enterCurrencySymbolPattern(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof PgNumericFormatListener ) ((PgNumericFormatListener)listener).exitCurrencySymbolPattern(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof PgNumericFormatVisitor ) return ((PgNumericFormatVisitor<? extends T>)visitor).visitCurrencySymbolPattern(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class DigitPatternContext extends PatternContext {
		public TerminalNode DIGIT_CAN_DROP() { return getToken(PgNumericFormatParser.DIGIT_CAN_DROP, 0); }
		public TerminalNode DIGIT_CAN_NOT_DROP() { return getToken(PgNumericFormatParser.DIGIT_CAN_NOT_DROP, 0); }
		public DigitPatternContext(PatternContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof PgNumericFormatListener ) ((PgNumericFormatListener)listener).enterDigitPattern(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof PgNumericFormatListener ) ((PgNumericFormatListener)listener).exitDigitPattern(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof PgNumericFormatVisitor ) return ((PgNumericFormatVisitor<? extends T>)visitor).visitDigitPattern(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class DecimalPointPatternContext extends PatternContext {
		public TerminalNode DECIMAL_POINT() { return getToken(PgNumericFormatParser.DECIMAL_POINT, 0); }
		public TerminalNode DECIMAL_POINT_LOCALE() { return getToken(PgNumericFormatParser.DECIMAL_POINT_LOCALE, 0); }
		public DecimalPointPatternContext(PatternContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof PgNumericFormatListener ) ((PgNumericFormatListener)listener).enterDecimalPointPattern(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof PgNumericFormatListener ) ((PgNumericFormatListener)listener).exitDecimalPointPattern(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof PgNumericFormatVisitor ) return ((PgNumericFormatVisitor<? extends T>)visitor).visitDecimalPointPattern(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class GroupSeparatorPatternContext extends PatternContext {
		public TerminalNode GROUP_SEPARATOR() { return getToken(PgNumericFormatParser.GROUP_SEPARATOR, 0); }
		public TerminalNode GROUP_SEPARATOR_LOCALE() { return getToken(PgNumericFormatParser.GROUP_SEPARATOR_LOCALE, 0); }
		public GroupSeparatorPatternContext(PatternContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof PgNumericFormatListener ) ((PgNumericFormatListener)listener).enterGroupSeparatorPattern(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof PgNumericFormatListener ) ((PgNumericFormatListener)listener).exitGroupSeparatorPattern(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof PgNumericFormatVisitor ) return ((PgNumericFormatVisitor<? extends T>)visitor).visitGroupSeparatorPattern(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class NonReservedPatternContext extends PatternContext {
		public NonReservedContext nonReserved() {
			return getRuleContext(NonReservedContext.class,0);
		}
		public NonReservedPatternContext(PatternContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof PgNumericFormatListener ) ((PgNumericFormatListener)listener).enterNonReservedPattern(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof PgNumericFormatListener ) ((PgNumericFormatListener)listener).exitNonReservedPattern(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof PgNumericFormatVisitor ) return ((PgNumericFormatVisitor<? extends T>)visitor).visitNonReservedPattern(this);
			else return visitor.visitChildren(this);
		}
	}

	public final PatternContext pattern() throws RecognitionException {
		PatternContext _localctx = new PatternContext(_ctx, getState());
		enterRule(_localctx, 2, RULE_pattern);
		try {
			setState(22);
			_errHandler.sync(this);
			switch (_input.LA(1)) {
			case DIGIT_CAN_DROP:
				_localctx = new DigitPatternContext(_localctx);
				enterOuterAlt(_localctx, 1);
				{
				setState(13);
				match(DIGIT_CAN_DROP);
				}
				break;
			case DIGIT_CAN_NOT_DROP:
				_localctx = new DigitPatternContext(_localctx);
				enterOuterAlt(_localctx, 2);
				{
				setState(14);
				match(DIGIT_CAN_NOT_DROP);
				}
				break;
			case DECIMAL_POINT:
				_localctx = new DecimalPointPatternContext(_localctx);
				enterOuterAlt(_localctx, 3);
				{
				setState(15);
				match(DECIMAL_POINT);
				}
				break;
			case DECIMAL_POINT_LOCALE:
				_localctx = new DecimalPointPatternContext(_localctx);
				enterOuterAlt(_localctx, 4);
				{
				setState(16);
				match(DECIMAL_POINT_LOCALE);
				}
				break;
			case GROUP_SEPARATOR:
				_localctx = new GroupSeparatorPatternContext(_localctx);
				enterOuterAlt(_localctx, 5);
				{
				setState(17);
				match(GROUP_SEPARATOR);
				}
				break;
			case GROUP_SEPARATOR_LOCALE:
				_localctx = new GroupSeparatorPatternContext(_localctx);
				enterOuterAlt(_localctx, 6);
				{
				setState(18);
				match(GROUP_SEPARATOR_LOCALE);
				}
				break;
			case CURRENCY_SYMBOL:
				_localctx = new CurrencySymbolPatternContext(_localctx);
				enterOuterAlt(_localctx, 7);
				{
				setState(19);
				match(CURRENCY_SYMBOL);
				}
				break;
			case EXPONENT:
				_localctx = new ExponentPatternContext(_localctx);
				enterOuterAlt(_localctx, 8);
				{
				setState(20);
				match(EXPONENT);
				}
				break;
			case PR:
			case SIGN_ANCHOR_LOCALE:
			case MINUS:
			case PLUS:
			case SIGN:
			case ROMAN:
			case ORDINAL:
			case SHIFT_DIGIT:
			case FM:
				_localctx = new NonReservedPatternContext(_localctx);
				enterOuterAlt(_localctx, 9);
				{
				setState(21);
				nonReserved();
				}
				break;
			default:
				throw new NoViableAltException(this);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class NonReservedContext extends ParserRuleContext {
		public TerminalNode PR() { return getToken(PgNumericFormatParser.PR, 0); }
		public TerminalNode SHIFT_DIGIT() { return getToken(PgNumericFormatParser.SHIFT_DIGIT, 0); }
		public TerminalNode ORDINAL() { return getToken(PgNumericFormatParser.ORDINAL, 0); }
		public TerminalNode ROMAN() { return getToken(PgNumericFormatParser.ROMAN, 0); }
		public TerminalNode PLUS() { return getToken(PgNumericFormatParser.PLUS, 0); }
		public TerminalNode MINUS() { return getToken(PgNumericFormatParser.MINUS, 0); }
		public TerminalNode SIGN() { return getToken(PgNumericFormatParser.SIGN, 0); }
		public TerminalNode SIGN_ANCHOR_LOCALE() { return getToken(PgNumericFormatParser.SIGN_ANCHOR_LOCALE, 0); }
		public TerminalNode FM() { return getToken(PgNumericFormatParser.FM, 0); }
		public NonReservedContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_nonReserved; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof PgNumericFormatListener ) ((PgNumericFormatListener)listener).enterNonReserved(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof PgNumericFormatListener ) ((PgNumericFormatListener)listener).exitNonReserved(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof PgNumericFormatVisitor ) return ((PgNumericFormatVisitor<? extends T>)visitor).visitNonReserved(this);
			else return visitor.visitChildren(this);
		}
	}

	public final NonReservedContext nonReserved() throws RecognitionException {
		NonReservedContext _localctx = new NonReservedContext(_ctx, getState());
		enterRule(_localctx, 4, RULE_nonReserved);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(24);
			_la = _input.LA(1);
			if ( !((((_la) & ~0x3f) == 0 && ((1L << _la) & 195680L) != 0)) ) {
			_errHandler.recoverInline(this);
			}
			else {
				if ( _input.LA(1)==Token.EOF ) matchedEOF = true;
				_errHandler.reportMatch(this);
				consume();
			}
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static final String _serializedATN =
		"\u0004\u0001\u0011\u001b\u0002\u0000\u0007\u0000\u0002\u0001\u0007\u0001"+
		"\u0002\u0002\u0007\u0002\u0001\u0000\u0001\u0000\u0005\u0000\t\b\u0000"+
		"\n\u0000\f\u0000\f\t\u0000\u0001\u0001\u0001\u0001\u0001\u0001\u0001\u0001"+
		"\u0001\u0001\u0001\u0001\u0001\u0001\u0001\u0001\u0001\u0001\u0003\u0001"+
		"\u0017\b\u0001\u0001\u0002\u0001\u0002\u0001\u0002\u0000\u0000\u0003\u0000"+
		"\u0002\u0004\u0000\u0001\u0003\u0000\u0005\u0006\n\u000f\u0011\u0011 "+
		"\u0000\u0006\u0001\u0000\u0000\u0000\u0002\u0016\u0001\u0000\u0000\u0000"+
		"\u0004\u0018\u0001\u0000\u0000\u0000\u0006\n\u0003\u0002\u0001\u0000\u0007"+
		"\t\u0003\u0002\u0001\u0000\b\u0007\u0001\u0000\u0000\u0000\t\f\u0001\u0000"+
		"\u0000\u0000\n\b\u0001\u0000\u0000\u0000\n\u000b\u0001\u0000\u0000\u0000"+
		"\u000b\u0001\u0001\u0000\u0000\u0000\f\n\u0001\u0000\u0000\u0000\r\u0017"+
		"\u0005\u0001\u0000\u0000\u000e\u0017\u0005\u0002\u0000\u0000\u000f\u0017"+
		"\u0005\u0003\u0000\u0000\u0010\u0017\u0005\b\u0000\u0000\u0011\u0017\u0005"+
		"\u0004\u0000\u0000\u0012\u0017\u0005\t\u0000\u0000\u0013\u0017\u0005\u0007"+
		"\u0000\u0000\u0014\u0017\u0005\u0010\u0000\u0000\u0015\u0017\u0003\u0004"+
		"\u0002\u0000\u0016\r\u0001\u0000\u0000\u0000\u0016\u000e\u0001\u0000\u0000"+
		"\u0000\u0016\u000f\u0001\u0000\u0000\u0000\u0016\u0010\u0001\u0000\u0000"+
		"\u0000\u0016\u0011\u0001\u0000\u0000\u0000\u0016\u0012\u0001\u0000\u0000"+
		"\u0000\u0016\u0013\u0001\u0000\u0000\u0000\u0016\u0014\u0001\u0000\u0000"+
		"\u0000\u0016\u0015\u0001\u0000\u0000\u0000\u0017\u0003\u0001\u0000\u0000"+
		"\u0000\u0018\u0019\u0007\u0000\u0000\u0000\u0019\u0005\u0001\u0000\u0000"+
		"\u0000\u0002\n\u0016";
	public static final ATN _ATN =
		new ATNDeserializer().deserialize(_serializedATN.toCharArray());
	static {
		_decisionToDFA = new DFA[_ATN.getNumberOfDecisions()];
		for (int i = 0; i < _ATN.getNumberOfDecisions(); i++) {
			_decisionToDFA[i] = new DFA(_ATN.getDecisionState(i), i);
		}
	}
}