// Generated from io/wren/base/type/parser/antlr/v4/PgDateTimeFormat.g4 by ANTLR 4.13.2
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
public class PgDateTimeFormatParser extends Parser {
	static { RuntimeMetaData.checkVersion("4.13.2", RuntimeMetaData.VERSION); }

	protected static final DFA[] _decisionToDFA;
	protected static final PredictionContextCache _sharedContextCache =
		new PredictionContextCache();
	public static final int
		HOUR=1, MINUTE=2, SECOND=3, MILLISECOND=4, YEAR=5, MONTH=6, DAY=7, WEEK=8, 
		TIME_ZONE=9, AM=10, PM=11, BC=12, AD=13, SEPARATOR=14;
	public static final int
		RULE_format = 0, RULE_symbol = 1, RULE_pattern = 2, RULE_separator = 3;
	private static String[] makeRuleNames() {
		return new String[] {
			"format", "symbol", "pattern", "separator"
		};
	}
	public static final String[] ruleNames = makeRuleNames();

	private static String[] makeLiteralNames() {
		return new String[] {
			null, null, null, null, null, null, null, null, null, "'TZ'"
		};
	}
	private static final String[] _LITERAL_NAMES = makeLiteralNames();
	private static String[] makeSymbolicNames() {
		return new String[] {
			null, "HOUR", "MINUTE", "SECOND", "MILLISECOND", "YEAR", "MONTH", "DAY", 
			"WEEK", "TIME_ZONE", "AM", "PM", "BC", "AD", "SEPARATOR"
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
	public String getGrammarFileName() { return "PgDateTimeFormat.g4"; }

	@Override
	public String[] getRuleNames() { return ruleNames; }

	@Override
	public String getSerializedATN() { return _serializedATN; }

	@Override
	public ATN getATN() { return _ATN; }

	public PgDateTimeFormatParser(TokenStream input) {
		super(input);
		_interp = new ParserATNSimulator(this,_ATN,_decisionToDFA,_sharedContextCache);
	}

	@SuppressWarnings("CheckReturnValue")
	public static class FormatContext extends ParserRuleContext {
		public List<SymbolContext> symbol() {
			return getRuleContexts(SymbolContext.class);
		}
		public SymbolContext symbol(int i) {
			return getRuleContext(SymbolContext.class,i);
		}
		public FormatContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_format; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof PgDateTimeFormatListener ) ((PgDateTimeFormatListener)listener).enterFormat(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof PgDateTimeFormatListener ) ((PgDateTimeFormatListener)listener).exitFormat(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof PgDateTimeFormatVisitor ) return ((PgDateTimeFormatVisitor<? extends T>)visitor).visitFormat(this);
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
			setState(8);
			symbol();
			setState(12);
			_errHandler.sync(this);
			_la = _input.LA(1);
			while ((((_la) & ~0x3f) == 0 && ((1L << _la) & 32766L) != 0)) {
				{
				{
				setState(9);
				symbol();
				}
				}
				setState(14);
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
	public static class SymbolContext extends ParserRuleContext {
		public SeparatorContext separator() {
			return getRuleContext(SeparatorContext.class,0);
		}
		public PatternContext pattern() {
			return getRuleContext(PatternContext.class,0);
		}
		public SymbolContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_symbol; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof PgDateTimeFormatListener ) ((PgDateTimeFormatListener)listener).enterSymbol(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof PgDateTimeFormatListener ) ((PgDateTimeFormatListener)listener).exitSymbol(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof PgDateTimeFormatVisitor ) return ((PgDateTimeFormatVisitor<? extends T>)visitor).visitSymbol(this);
			else return visitor.visitChildren(this);
		}
	}

	public final SymbolContext symbol() throws RecognitionException {
		SymbolContext _localctx = new SymbolContext(_ctx, getState());
		enterRule(_localctx, 2, RULE_symbol);
		try {
			setState(17);
			_errHandler.sync(this);
			switch (_input.LA(1)) {
			case SEPARATOR:
				enterOuterAlt(_localctx, 1);
				{
				setState(15);
				separator();
				}
				break;
			case HOUR:
			case MINUTE:
			case SECOND:
			case MILLISECOND:
			case YEAR:
			case MONTH:
			case DAY:
			case WEEK:
			case TIME_ZONE:
			case AM:
			case PM:
			case BC:
			case AD:
				enterOuterAlt(_localctx, 2);
				{
				setState(16);
				pattern();
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
	public static class MilliSecondLiteralContext extends PatternContext {
		public TerminalNode MILLISECOND() { return getToken(PgDateTimeFormatParser.MILLISECOND, 0); }
		public MilliSecondLiteralContext(PatternContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof PgDateTimeFormatListener ) ((PgDateTimeFormatListener)listener).enterMilliSecondLiteral(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof PgDateTimeFormatListener ) ((PgDateTimeFormatListener)listener).exitMilliSecondLiteral(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof PgDateTimeFormatVisitor ) return ((PgDateTimeFormatVisitor<? extends T>)visitor).visitMilliSecondLiteral(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class WeekLiteralContext extends PatternContext {
		public TerminalNode WEEK() { return getToken(PgDateTimeFormatParser.WEEK, 0); }
		public WeekLiteralContext(PatternContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof PgDateTimeFormatListener ) ((PgDateTimeFormatListener)listener).enterWeekLiteral(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof PgDateTimeFormatListener ) ((PgDateTimeFormatListener)listener).exitWeekLiteral(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof PgDateTimeFormatVisitor ) return ((PgDateTimeFormatVisitor<? extends T>)visitor).visitWeekLiteral(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class MinuteLiteralContext extends PatternContext {
		public TerminalNode MINUTE() { return getToken(PgDateTimeFormatParser.MINUTE, 0); }
		public MinuteLiteralContext(PatternContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof PgDateTimeFormatListener ) ((PgDateTimeFormatListener)listener).enterMinuteLiteral(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof PgDateTimeFormatListener ) ((PgDateTimeFormatListener)listener).exitMinuteLiteral(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof PgDateTimeFormatVisitor ) return ((PgDateTimeFormatVisitor<? extends T>)visitor).visitMinuteLiteral(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class DayLiteralContext extends PatternContext {
		public TerminalNode DAY() { return getToken(PgDateTimeFormatParser.DAY, 0); }
		public DayLiteralContext(PatternContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof PgDateTimeFormatListener ) ((PgDateTimeFormatListener)listener).enterDayLiteral(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof PgDateTimeFormatListener ) ((PgDateTimeFormatListener)listener).exitDayLiteral(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof PgDateTimeFormatVisitor ) return ((PgDateTimeFormatVisitor<? extends T>)visitor).visitDayLiteral(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class MeridiemMarkerLiteralContext extends PatternContext {
		public TerminalNode AM() { return getToken(PgDateTimeFormatParser.AM, 0); }
		public TerminalNode PM() { return getToken(PgDateTimeFormatParser.PM, 0); }
		public MeridiemMarkerLiteralContext(PatternContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof PgDateTimeFormatListener ) ((PgDateTimeFormatListener)listener).enterMeridiemMarkerLiteral(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof PgDateTimeFormatListener ) ((PgDateTimeFormatListener)listener).exitMeridiemMarkerLiteral(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof PgDateTimeFormatVisitor ) return ((PgDateTimeFormatVisitor<? extends T>)visitor).visitMeridiemMarkerLiteral(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class SecondLiteralContext extends PatternContext {
		public TerminalNode SECOND() { return getToken(PgDateTimeFormatParser.SECOND, 0); }
		public SecondLiteralContext(PatternContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof PgDateTimeFormatListener ) ((PgDateTimeFormatListener)listener).enterSecondLiteral(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof PgDateTimeFormatListener ) ((PgDateTimeFormatListener)listener).exitSecondLiteral(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof PgDateTimeFormatVisitor ) return ((PgDateTimeFormatVisitor<? extends T>)visitor).visitSecondLiteral(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class YearLiteralContext extends PatternContext {
		public TerminalNode YEAR() { return getToken(PgDateTimeFormatParser.YEAR, 0); }
		public YearLiteralContext(PatternContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof PgDateTimeFormatListener ) ((PgDateTimeFormatListener)listener).enterYearLiteral(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof PgDateTimeFormatListener ) ((PgDateTimeFormatListener)listener).exitYearLiteral(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof PgDateTimeFormatVisitor ) return ((PgDateTimeFormatVisitor<? extends T>)visitor).visitYearLiteral(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class HourLiteralContext extends PatternContext {
		public TerminalNode HOUR() { return getToken(PgDateTimeFormatParser.HOUR, 0); }
		public HourLiteralContext(PatternContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof PgDateTimeFormatListener ) ((PgDateTimeFormatListener)listener).enterHourLiteral(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof PgDateTimeFormatListener ) ((PgDateTimeFormatListener)listener).exitHourLiteral(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof PgDateTimeFormatVisitor ) return ((PgDateTimeFormatVisitor<? extends T>)visitor).visitHourLiteral(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class EraDesignatorLiteralContext extends PatternContext {
		public TerminalNode BC() { return getToken(PgDateTimeFormatParser.BC, 0); }
		public TerminalNode AD() { return getToken(PgDateTimeFormatParser.AD, 0); }
		public EraDesignatorLiteralContext(PatternContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof PgDateTimeFormatListener ) ((PgDateTimeFormatListener)listener).enterEraDesignatorLiteral(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof PgDateTimeFormatListener ) ((PgDateTimeFormatListener)listener).exitEraDesignatorLiteral(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof PgDateTimeFormatVisitor ) return ((PgDateTimeFormatVisitor<? extends T>)visitor).visitEraDesignatorLiteral(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class MonthLiteralContext extends PatternContext {
		public TerminalNode MONTH() { return getToken(PgDateTimeFormatParser.MONTH, 0); }
		public MonthLiteralContext(PatternContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof PgDateTimeFormatListener ) ((PgDateTimeFormatListener)listener).enterMonthLiteral(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof PgDateTimeFormatListener ) ((PgDateTimeFormatListener)listener).exitMonthLiteral(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof PgDateTimeFormatVisitor ) return ((PgDateTimeFormatVisitor<? extends T>)visitor).visitMonthLiteral(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class TimeZoneLiteralContext extends PatternContext {
		public TerminalNode TIME_ZONE() { return getToken(PgDateTimeFormatParser.TIME_ZONE, 0); }
		public TimeZoneLiteralContext(PatternContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof PgDateTimeFormatListener ) ((PgDateTimeFormatListener)listener).enterTimeZoneLiteral(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof PgDateTimeFormatListener ) ((PgDateTimeFormatListener)listener).exitTimeZoneLiteral(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof PgDateTimeFormatVisitor ) return ((PgDateTimeFormatVisitor<? extends T>)visitor).visitTimeZoneLiteral(this);
			else return visitor.visitChildren(this);
		}
	}

	public final PatternContext pattern() throws RecognitionException {
		PatternContext _localctx = new PatternContext(_ctx, getState());
		enterRule(_localctx, 4, RULE_pattern);
		try {
			setState(32);
			_errHandler.sync(this);
			switch (_input.LA(1)) {
			case HOUR:
				_localctx = new HourLiteralContext(_localctx);
				enterOuterAlt(_localctx, 1);
				{
				setState(19);
				match(HOUR);
				}
				break;
			case MINUTE:
				_localctx = new MinuteLiteralContext(_localctx);
				enterOuterAlt(_localctx, 2);
				{
				setState(20);
				match(MINUTE);
				}
				break;
			case SECOND:
				_localctx = new SecondLiteralContext(_localctx);
				enterOuterAlt(_localctx, 3);
				{
				setState(21);
				match(SECOND);
				}
				break;
			case MILLISECOND:
				_localctx = new MilliSecondLiteralContext(_localctx);
				enterOuterAlt(_localctx, 4);
				{
				setState(22);
				match(MILLISECOND);
				}
				break;
			case YEAR:
				_localctx = new YearLiteralContext(_localctx);
				enterOuterAlt(_localctx, 5);
				{
				setState(23);
				match(YEAR);
				}
				break;
			case MONTH:
				_localctx = new MonthLiteralContext(_localctx);
				enterOuterAlt(_localctx, 6);
				{
				setState(24);
				match(MONTH);
				}
				break;
			case DAY:
				_localctx = new DayLiteralContext(_localctx);
				enterOuterAlt(_localctx, 7);
				{
				setState(25);
				match(DAY);
				}
				break;
			case WEEK:
				_localctx = new WeekLiteralContext(_localctx);
				enterOuterAlt(_localctx, 8);
				{
				setState(26);
				match(WEEK);
				}
				break;
			case TIME_ZONE:
				_localctx = new TimeZoneLiteralContext(_localctx);
				enterOuterAlt(_localctx, 9);
				{
				setState(27);
				match(TIME_ZONE);
				}
				break;
			case AM:
				_localctx = new MeridiemMarkerLiteralContext(_localctx);
				enterOuterAlt(_localctx, 10);
				{
				setState(28);
				match(AM);
				}
				break;
			case PM:
				_localctx = new MeridiemMarkerLiteralContext(_localctx);
				enterOuterAlt(_localctx, 11);
				{
				setState(29);
				match(PM);
				}
				break;
			case BC:
				_localctx = new EraDesignatorLiteralContext(_localctx);
				enterOuterAlt(_localctx, 12);
				{
				setState(30);
				match(BC);
				}
				break;
			case AD:
				_localctx = new EraDesignatorLiteralContext(_localctx);
				enterOuterAlt(_localctx, 13);
				{
				setState(31);
				match(AD);
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
	public static class SeparatorContext extends ParserRuleContext {
		public TerminalNode SEPARATOR() { return getToken(PgDateTimeFormatParser.SEPARATOR, 0); }
		public SeparatorContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_separator; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof PgDateTimeFormatListener ) ((PgDateTimeFormatListener)listener).enterSeparator(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof PgDateTimeFormatListener ) ((PgDateTimeFormatListener)listener).exitSeparator(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof PgDateTimeFormatVisitor ) return ((PgDateTimeFormatVisitor<? extends T>)visitor).visitSeparator(this);
			else return visitor.visitChildren(this);
		}
	}

	public final SeparatorContext separator() throws RecognitionException {
		SeparatorContext _localctx = new SeparatorContext(_ctx, getState());
		enterRule(_localctx, 6, RULE_separator);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(34);
			match(SEPARATOR);
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
		"\u0004\u0001\u000e%\u0002\u0000\u0007\u0000\u0002\u0001\u0007\u0001\u0002"+
		"\u0002\u0007\u0002\u0002\u0003\u0007\u0003\u0001\u0000\u0001\u0000\u0005"+
		"\u0000\u000b\b\u0000\n\u0000\f\u0000\u000e\t\u0000\u0001\u0001\u0001\u0001"+
		"\u0003\u0001\u0012\b\u0001\u0001\u0002\u0001\u0002\u0001\u0002\u0001\u0002"+
		"\u0001\u0002\u0001\u0002\u0001\u0002\u0001\u0002\u0001\u0002\u0001\u0002"+
		"\u0001\u0002\u0001\u0002\u0001\u0002\u0003\u0002!\b\u0002\u0001\u0003"+
		"\u0001\u0003\u0001\u0003\u0000\u0000\u0004\u0000\u0002\u0004\u0006\u0000"+
		"\u0000.\u0000\b\u0001\u0000\u0000\u0000\u0002\u0011\u0001\u0000\u0000"+
		"\u0000\u0004 \u0001\u0000\u0000\u0000\u0006\"\u0001\u0000\u0000\u0000"+
		"\b\f\u0003\u0002\u0001\u0000\t\u000b\u0003\u0002\u0001\u0000\n\t\u0001"+
		"\u0000\u0000\u0000\u000b\u000e\u0001\u0000\u0000\u0000\f\n\u0001\u0000"+
		"\u0000\u0000\f\r\u0001\u0000\u0000\u0000\r\u0001\u0001\u0000\u0000\u0000"+
		"\u000e\f\u0001\u0000\u0000\u0000\u000f\u0012\u0003\u0006\u0003\u0000\u0010"+
		"\u0012\u0003\u0004\u0002\u0000\u0011\u000f\u0001\u0000\u0000\u0000\u0011"+
		"\u0010\u0001\u0000\u0000\u0000\u0012\u0003\u0001\u0000\u0000\u0000\u0013"+
		"!\u0005\u0001\u0000\u0000\u0014!\u0005\u0002\u0000\u0000\u0015!\u0005"+
		"\u0003\u0000\u0000\u0016!\u0005\u0004\u0000\u0000\u0017!\u0005\u0005\u0000"+
		"\u0000\u0018!\u0005\u0006\u0000\u0000\u0019!\u0005\u0007\u0000\u0000\u001a"+
		"!\u0005\b\u0000\u0000\u001b!\u0005\t\u0000\u0000\u001c!\u0005\n\u0000"+
		"\u0000\u001d!\u0005\u000b\u0000\u0000\u001e!\u0005\f\u0000\u0000\u001f"+
		"!\u0005\r\u0000\u0000 \u0013\u0001\u0000\u0000\u0000 \u0014\u0001\u0000"+
		"\u0000\u0000 \u0015\u0001\u0000\u0000\u0000 \u0016\u0001\u0000\u0000\u0000"+
		" \u0017\u0001\u0000\u0000\u0000 \u0018\u0001\u0000\u0000\u0000 \u0019"+
		"\u0001\u0000\u0000\u0000 \u001a\u0001\u0000\u0000\u0000 \u001b\u0001\u0000"+
		"\u0000\u0000 \u001c\u0001\u0000\u0000\u0000 \u001d\u0001\u0000\u0000\u0000"+
		" \u001e\u0001\u0000\u0000\u0000 \u001f\u0001\u0000\u0000\u0000!\u0005"+
		"\u0001\u0000\u0000\u0000\"#\u0005\u000e\u0000\u0000#\u0007\u0001\u0000"+
		"\u0000\u0000\u0003\f\u0011 ";
	public static final ATN _ATN =
		new ATNDeserializer().deserialize(_serializedATN.toCharArray());
	static {
		_decisionToDFA = new DFA[_ATN.getNumberOfDecisions()];
		for (int i = 0; i < _ATN.getNumberOfDecisions(); i++) {
			_decisionToDFA[i] = new DFA(_ATN.getDecisionState(i), i);
		}
	}
}