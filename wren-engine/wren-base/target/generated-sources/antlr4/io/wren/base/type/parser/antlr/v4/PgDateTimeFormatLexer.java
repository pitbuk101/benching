// Generated from io/wren/base/type/parser/antlr/v4/PgDateTimeFormat.g4 by ANTLR 4.13.2
package io.wren.base.type.parser.antlr.v4;
import org.antlr.v4.runtime.Lexer;
import org.antlr.v4.runtime.CharStream;
import org.antlr.v4.runtime.Token;
import org.antlr.v4.runtime.TokenStream;
import org.antlr.v4.runtime.*;
import org.antlr.v4.runtime.atn.*;
import org.antlr.v4.runtime.dfa.DFA;
import org.antlr.v4.runtime.misc.*;

@SuppressWarnings({"all", "warnings", "unchecked", "unused", "cast", "CheckReturnValue", "this-escape"})
public class PgDateTimeFormatLexer extends Lexer {
	static { RuntimeMetaData.checkVersion("4.13.2", RuntimeMetaData.VERSION); }

	protected static final DFA[] _decisionToDFA;
	protected static final PredictionContextCache _sharedContextCache =
		new PredictionContextCache();
	public static final int
		HOUR=1, MINUTE=2, SECOND=3, MILLISECOND=4, YEAR=5, MONTH=6, DAY=7, WEEK=8, 
		TIME_ZONE=9, AM=10, PM=11, BC=12, AD=13, SEPARATOR=14;
	public static String[] channelNames = {
		"DEFAULT_TOKEN_CHANNEL", "HIDDEN"
	};

	public static String[] modeNames = {
		"DEFAULT_MODE"
	};

	private static String[] makeRuleNames() {
		return new String[] {
			"HOUR", "MINUTE", "SECOND", "MILLISECOND", "YEAR", "MONTH", "DAY", "WEEK", 
			"TIME_ZONE", "AM", "PM", "BC", "AD", "SEPARATOR"
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


	public PgDateTimeFormatLexer(CharStream input) {
		super(input);
		_interp = new LexerATNSimulator(this,_ATN,_decisionToDFA,_sharedContextCache);
	}

	@Override
	public String getGrammarFileName() { return "PgDateTimeFormat.g4"; }

	@Override
	public String[] getRuleNames() { return ruleNames; }

	@Override
	public String getSerializedATN() { return _serializedATN; }

	@Override
	public String[] getChannelNames() { return channelNames; }

	@Override
	public String[] getModeNames() { return modeNames; }

	@Override
	public ATN getATN() { return _ATN; }

	public static final String _serializedATN =
		"\u0004\u0000\u000e\u0099\u0006\uffff\uffff\u0002\u0000\u0007\u0000\u0002"+
		"\u0001\u0007\u0001\u0002\u0002\u0007\u0002\u0002\u0003\u0007\u0003\u0002"+
		"\u0004\u0007\u0004\u0002\u0005\u0007\u0005\u0002\u0006\u0007\u0006\u0002"+
		"\u0007\u0007\u0007\u0002\b\u0007\b\u0002\t\u0007\t\u0002\n\u0007\n\u0002"+
		"\u000b\u0007\u000b\u0002\f\u0007\f\u0002\r\u0007\r\u0001\u0000\u0001\u0000"+
		"\u0001\u0000\u0001\u0000\u0003\u0000\"\b\u0000\u0001\u0000\u0001\u0000"+
		"\u0001\u0000\u0001\u0000\u0003\u0000(\b\u0000\u0001\u0001\u0001\u0001"+
		"\u0001\u0001\u0001\u0001\u0003\u0001.\b\u0001\u0001\u0002\u0001\u0002"+
		"\u0001\u0002\u0001\u0002\u0003\u00024\b\u0002\u0001\u0003\u0001\u0003"+
		"\u0001\u0003\u0001\u0003\u0001\u0003\u0001\u0003\u0001\u0003\u0001\u0003"+
		"\u0001\u0003\u0001\u0003\u0003\u0003@\b\u0003\u0001\u0004\u0001\u0004"+
		"\u0001\u0004\u0001\u0004\u0001\u0004\u0001\u0004\u0001\u0004\u0001\u0004"+
		"\u0001\u0004\u0001\u0004\u0001\u0004\u0001\u0004\u0001\u0004\u0001\u0004"+
		"\u0001\u0004\u0001\u0004\u0001\u0004\u0001\u0004\u0001\u0004\u0003\u0004"+
		"U\b\u0004\u0001\u0005\u0001\u0005\u0001\u0005\u0001\u0005\u0001\u0005"+
		"\u0001\u0005\u0001\u0005\u0001\u0005\u0001\u0005\u0001\u0005\u0001\u0005"+
		"\u0001\u0005\u0003\u0005c\b\u0005\u0001\u0006\u0001\u0006\u0001\u0006"+
		"\u0001\u0006\u0001\u0006\u0001\u0006\u0001\u0006\u0001\u0006\u0001\u0006"+
		"\u0001\u0006\u0001\u0006\u0001\u0006\u0001\u0006\u0001\u0006\u0001\u0006"+
		"\u0001\u0006\u0003\u0006u\b\u0006\u0001\u0007\u0001\u0007\u0001\u0007"+
		"\u0001\u0007\u0003\u0007{\b\u0007\u0001\b\u0001\b\u0001\b\u0001\t\u0001"+
		"\t\u0001\t\u0001\t\u0003\t\u0084\b\t\u0001\n\u0001\n\u0001\n\u0001\n\u0003"+
		"\n\u008a\b\n\u0001\u000b\u0001\u000b\u0001\u000b\u0001\u000b\u0003\u000b"+
		"\u0090\b\u000b\u0001\f\u0001\f\u0001\f\u0001\f\u0003\f\u0096\b\f\u0001"+
		"\r\u0001\r\u0000\u0000\u000e\u0001\u0001\u0003\u0002\u0005\u0003\u0007"+
		"\u0004\t\u0005\u000b\u0006\r\u0007\u000f\b\u0011\t\u0013\n\u0015\u000b"+
		"\u0017\f\u0019\r\u001b\u000e\u0001\u0000\u0003\u0002\u0000YYyy\u0002\u0000"+
		"DDdd\u0005\u0000  -/::\\\\__\u00b4\u0000\u0001\u0001\u0000\u0000\u0000"+
		"\u0000\u0003\u0001\u0000\u0000\u0000\u0000\u0005\u0001\u0000\u0000\u0000"+
		"\u0000\u0007\u0001\u0000\u0000\u0000\u0000\t\u0001\u0000\u0000\u0000\u0000"+
		"\u000b\u0001\u0000\u0000\u0000\u0000\r\u0001\u0000\u0000\u0000\u0000\u000f"+
		"\u0001\u0000\u0000\u0000\u0000\u0011\u0001\u0000\u0000\u0000\u0000\u0013"+
		"\u0001\u0000\u0000\u0000\u0000\u0015\u0001\u0000\u0000\u0000\u0000\u0017"+
		"\u0001\u0000\u0000\u0000\u0000\u0019\u0001\u0000\u0000\u0000\u0000\u001b"+
		"\u0001\u0000\u0000\u0000\u0001!\u0001\u0000\u0000\u0000\u0003-\u0001\u0000"+
		"\u0000\u0000\u00053\u0001\u0000\u0000\u0000\u0007?\u0001\u0000\u0000\u0000"+
		"\tT\u0001\u0000\u0000\u0000\u000bb\u0001\u0000\u0000\u0000\rt\u0001\u0000"+
		"\u0000\u0000\u000fz\u0001\u0000\u0000\u0000\u0011|\u0001\u0000\u0000\u0000"+
		"\u0013\u0083\u0001\u0000\u0000\u0000\u0015\u0089\u0001\u0000\u0000\u0000"+
		"\u0017\u008f\u0001\u0000\u0000\u0000\u0019\u0095\u0001\u0000\u0000\u0000"+
		"\u001b\u0097\u0001\u0000\u0000\u0000\u001d\u001e\u0005H\u0000\u0000\u001e"+
		"\"\u0005H\u0000\u0000\u001f \u0005h\u0000\u0000 \"\u0005h\u0000\u0000"+
		"!\u001d\u0001\u0000\u0000\u0000!\u001f\u0001\u0000\u0000\u0000\"\'\u0001"+
		"\u0000\u0000\u0000#$\u00051\u0000\u0000$(\u00052\u0000\u0000%&\u00052"+
		"\u0000\u0000&(\u00054\u0000\u0000\'#\u0001\u0000\u0000\u0000\'%\u0001"+
		"\u0000\u0000\u0000\'(\u0001\u0000\u0000\u0000(\u0002\u0001\u0000\u0000"+
		"\u0000)*\u0005M\u0000\u0000*.\u0005I\u0000\u0000+,\u0005m\u0000\u0000"+
		",.\u0005i\u0000\u0000-)\u0001\u0000\u0000\u0000-+\u0001\u0000\u0000\u0000"+
		".\u0004\u0001\u0000\u0000\u0000/0\u0005S\u0000\u000004\u0005S\u0000\u0000"+
		"12\u0005s\u0000\u000024\u0005s\u0000\u00003/\u0001\u0000\u0000\u00003"+
		"1\u0001\u0000\u0000\u00004\u0006\u0001\u0000\u0000\u000056\u0005M\u0000"+
		"\u00006@\u0005S\u0000\u000078\u0005m\u0000\u00008@\u0005s\u0000\u0000"+
		"9:\u0005F\u0000\u0000:;\u0005F\u0000\u0000;@\u00053\u0000\u0000<=\u0005"+
		"f\u0000\u0000=>\u0005f\u0000\u0000>@\u00053\u0000\u0000?5\u0001\u0000"+
		"\u0000\u0000?7\u0001\u0000\u0000\u0000?9\u0001\u0000\u0000\u0000?<\u0001"+
		"\u0000\u0000\u0000@\b\u0001\u0000\u0000\u0000AB\u0005Y\u0000\u0000BC\u0005"+
		"Y\u0000\u0000CD\u0005Y\u0000\u0000DU\u0005Y\u0000\u0000EF\u0005y\u0000"+
		"\u0000FG\u0005y\u0000\u0000GH\u0005y\u0000\u0000HU\u0005y\u0000\u0000"+
		"IJ\u0005Y\u0000\u0000JK\u0005Y\u0000\u0000KU\u0005Y\u0000\u0000LM\u0005"+
		"y\u0000\u0000MN\u0005y\u0000\u0000NU\u0005y\u0000\u0000OP\u0005Y\u0000"+
		"\u0000PU\u0005Y\u0000\u0000QR\u0005y\u0000\u0000RU\u0005y\u0000\u0000"+
		"SU\u0007\u0000\u0000\u0000TA\u0001\u0000\u0000\u0000TE\u0001\u0000\u0000"+
		"\u0000TI\u0001\u0000\u0000\u0000TL\u0001\u0000\u0000\u0000TO\u0001\u0000"+
		"\u0000\u0000TQ\u0001\u0000\u0000\u0000TS\u0001\u0000\u0000\u0000U\n\u0001"+
		"\u0000\u0000\u0000VW\u0005M\u0000\u0000Wc\u0005M\u0000\u0000XY\u0005m"+
		"\u0000\u0000Yc\u0005m\u0000\u0000Z[\u0005M\u0000\u0000[\\\u0005o\u0000"+
		"\u0000\\]\u0005n\u0000\u0000]^\u0005t\u0000\u0000^c\u0005h\u0000\u0000"+
		"_`\u0005M\u0000\u0000`a\u0005o\u0000\u0000ac\u0005n\u0000\u0000bV\u0001"+
		"\u0000\u0000\u0000bX\u0001\u0000\u0000\u0000bZ\u0001\u0000\u0000\u0000"+
		"b_\u0001\u0000\u0000\u0000c\f\u0001\u0000\u0000\u0000de\u0005D\u0000\u0000"+
		"ef\u0005D\u0000\u0000fu\u0005D\u0000\u0000gh\u0005d\u0000\u0000hi\u0005"+
		"d\u0000\u0000iu\u0005d\u0000\u0000jk\u0005D\u0000\u0000ku\u0005D\u0000"+
		"\u0000lm\u0005d\u0000\u0000mu\u0005d\u0000\u0000nu\u0007\u0001\u0000\u0000"+
		"op\u0005D\u0000\u0000pq\u0005a\u0000\u0000qu\u0005y\u0000\u0000rs\u0005"+
		"D\u0000\u0000su\u0005y\u0000\u0000td\u0001\u0000\u0000\u0000tg\u0001\u0000"+
		"\u0000\u0000tj\u0001\u0000\u0000\u0000tl\u0001\u0000\u0000\u0000tn\u0001"+
		"\u0000\u0000\u0000to\u0001\u0000\u0000\u0000tr\u0001\u0000\u0000\u0000"+
		"u\u000e\u0001\u0000\u0000\u0000vw\u0005W\u0000\u0000w{\u0005W\u0000\u0000"+
		"xy\u0005w\u0000\u0000y{\u0005w\u0000\u0000zv\u0001\u0000\u0000\u0000z"+
		"x\u0001\u0000\u0000\u0000{\u0010\u0001\u0000\u0000\u0000|}\u0005T\u0000"+
		"\u0000}~\u0005Z\u0000\u0000~\u0012\u0001\u0000\u0000\u0000\u007f\u0080"+
		"\u0005A\u0000\u0000\u0080\u0084\u0005M\u0000\u0000\u0081\u0082\u0005a"+
		"\u0000\u0000\u0082\u0084\u0005m\u0000\u0000\u0083\u007f\u0001\u0000\u0000"+
		"\u0000\u0083\u0081\u0001\u0000\u0000\u0000\u0084\u0014\u0001\u0000\u0000"+
		"\u0000\u0085\u0086\u0005P\u0000\u0000\u0086\u008a\u0005M\u0000\u0000\u0087"+
		"\u0088\u0005p\u0000\u0000\u0088\u008a\u0005m\u0000\u0000\u0089\u0085\u0001"+
		"\u0000\u0000\u0000\u0089\u0087\u0001\u0000\u0000\u0000\u008a\u0016\u0001"+
		"\u0000\u0000\u0000\u008b\u008c\u0005B\u0000\u0000\u008c\u0090\u0005C\u0000"+
		"\u0000\u008d\u008e\u0005b\u0000\u0000\u008e\u0090\u0005c\u0000\u0000\u008f"+
		"\u008b\u0001\u0000\u0000\u0000\u008f\u008d\u0001\u0000\u0000\u0000\u0090"+
		"\u0018\u0001\u0000\u0000\u0000\u0091\u0092\u0005A\u0000\u0000\u0092\u0096"+
		"\u0005D\u0000\u0000\u0093\u0094\u0005a\u0000\u0000\u0094\u0096\u0005d"+
		"\u0000\u0000\u0095\u0091\u0001\u0000\u0000\u0000\u0095\u0093\u0001\u0000"+
		"\u0000\u0000\u0096\u001a\u0001\u0000\u0000\u0000\u0097\u0098\u0007\u0002"+
		"\u0000\u0000\u0098\u001c\u0001\u0000\u0000\u0000\u000e\u0000!\'-3?Tbt"+
		"z\u0083\u0089\u008f\u0095\u0000";
	public static final ATN _ATN =
		new ATNDeserializer().deserialize(_serializedATN.toCharArray());
	static {
		_decisionToDFA = new DFA[_ATN.getNumberOfDecisions()];
		for (int i = 0; i < _ATN.getNumberOfDecisions(); i++) {
			_decisionToDFA[i] = new DFA(_ATN.getDecisionState(i), i);
		}
	}
}