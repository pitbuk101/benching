// Generated from io/wren/base/type/parser/antlr/v4/PgArray.g4 by ANTLR 4.13.2
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
public class PgArrayLexer extends Lexer {
	static { RuntimeMetaData.checkVersion("4.13.2", RuntimeMetaData.VERSION); }

	protected static final DFA[] _decisionToDFA;
	protected static final PredictionContextCache _sharedContextCache =
		new PredictionContextCache();
	public static final int
		T__0=1, T__1=2, T__2=3, NULL=4, QUOTED_STRING=5, UNQUOTED_STRING=6, WS=7;
	public static String[] channelNames = {
		"DEFAULT_TOKEN_CHANNEL", "HIDDEN"
	};

	public static String[] modeNames = {
		"DEFAULT_MODE"
	};

	private static String[] makeRuleNames() {
		return new String[] {
			"T__0", "T__1", "T__2", "NULL", "QUOTED_STRING", "UNQUOTED_STRING", "CHAR", 
			"ESC", "UNICODE", "HEX", "WS"
		};
	}
	public static final String[] ruleNames = makeRuleNames();

	private static String[] makeLiteralNames() {
		return new String[] {
			null, "'{'", "','", "'}'"
		};
	}
	private static final String[] _LITERAL_NAMES = makeLiteralNames();
	private static String[] makeSymbolicNames() {
		return new String[] {
			null, null, null, null, "NULL", "QUOTED_STRING", "UNQUOTED_STRING", "WS"
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


	public PgArrayLexer(CharStream input) {
		super(input);
		_interp = new LexerATNSimulator(this,_ATN,_decisionToDFA,_sharedContextCache);
	}

	@Override
	public String getGrammarFileName() { return "PgArray.g4"; }

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
		"\u0004\u0000\u0007Y\u0006\uffff\uffff\u0002\u0000\u0007\u0000\u0002\u0001"+
		"\u0007\u0001\u0002\u0002\u0007\u0002\u0002\u0003\u0007\u0003\u0002\u0004"+
		"\u0007\u0004\u0002\u0005\u0007\u0005\u0002\u0006\u0007\u0006\u0002\u0007"+
		"\u0007\u0007\u0002\b\u0007\b\u0002\t\u0007\t\u0002\n\u0007\n\u0001\u0000"+
		"\u0001\u0000\u0001\u0001\u0001\u0001\u0001\u0002\u0001\u0002\u0001\u0003"+
		"\u0001\u0003\u0001\u0003\u0001\u0003\u0001\u0003\u0001\u0004\u0001\u0004"+
		"\u0001\u0004\u0005\u0004&\b\u0004\n\u0004\f\u0004)\t\u0004\u0001\u0004"+
		"\u0001\u0004\u0001\u0005\u0004\u0005.\b\u0005\u000b\u0005\f\u0005/\u0001"+
		"\u0005\u0005\u00053\b\u0005\n\u0005\f\u00056\t\u0005\u0001\u0005\u0004"+
		"\u00059\b\u0005\u000b\u0005\f\u0005:\u0001\u0005\u0004\u0005>\b\u0005"+
		"\u000b\u0005\f\u0005?\u0003\u0005B\b\u0005\u0001\u0006\u0001\u0006\u0001"+
		"\u0007\u0001\u0007\u0001\u0007\u0003\u0007I\b\u0007\u0001\b\u0001\b\u0001"+
		"\b\u0001\b\u0001\b\u0001\b\u0001\t\u0001\t\u0001\n\u0004\nT\b\n\u000b"+
		"\n\f\nU\u0001\n\u0001\n\u0000\u0000\u000b\u0001\u0001\u0003\u0002\u0005"+
		"\u0003\u0007\u0004\t\u0005\u000b\u0006\r\u0000\u000f\u0000\u0011\u0000"+
		"\u0013\u0000\u0015\u0007\u0001\u0000\b\u0002\u0000NNnn\u0002\u0000UUu"+
		"u\u0002\u0000LLll\u0002\u0000\"\"\\\\\b\u0000\t\n\r\r  \"\",,\\\\{{}}"+
		"\b\u0000\"\"//\\\\bbffnnrrtt\u0003\u000009AFaf\u0003\u0000\t\n\r\r  ]"+
		"\u0000\u0001\u0001\u0000\u0000\u0000\u0000\u0003\u0001\u0000\u0000\u0000"+
		"\u0000\u0005\u0001\u0000\u0000\u0000\u0000\u0007\u0001\u0000\u0000\u0000"+
		"\u0000\t\u0001\u0000\u0000\u0000\u0000\u000b\u0001\u0000\u0000\u0000\u0000"+
		"\u0015\u0001\u0000\u0000\u0000\u0001\u0017\u0001\u0000\u0000\u0000\u0003"+
		"\u0019\u0001\u0000\u0000\u0000\u0005\u001b\u0001\u0000\u0000\u0000\u0007"+
		"\u001d\u0001\u0000\u0000\u0000\t\"\u0001\u0000\u0000\u0000\u000bA\u0001"+
		"\u0000\u0000\u0000\rC\u0001\u0000\u0000\u0000\u000fE\u0001\u0000\u0000"+
		"\u0000\u0011J\u0001\u0000\u0000\u0000\u0013P\u0001\u0000\u0000\u0000\u0015"+
		"S\u0001\u0000\u0000\u0000\u0017\u0018\u0005{\u0000\u0000\u0018\u0002\u0001"+
		"\u0000\u0000\u0000\u0019\u001a\u0005,\u0000\u0000\u001a\u0004\u0001\u0000"+
		"\u0000\u0000\u001b\u001c\u0005}\u0000\u0000\u001c\u0006\u0001\u0000\u0000"+
		"\u0000\u001d\u001e\u0007\u0000\u0000\u0000\u001e\u001f\u0007\u0001\u0000"+
		"\u0000\u001f \u0007\u0002\u0000\u0000 !\u0007\u0002\u0000\u0000!\b\u0001"+
		"\u0000\u0000\u0000\"\'\u0005\"\u0000\u0000#&\u0003\u000f\u0007\u0000$"+
		"&\b\u0003\u0000\u0000%#\u0001\u0000\u0000\u0000%$\u0001\u0000\u0000\u0000"+
		"&)\u0001\u0000\u0000\u0000\'%\u0001\u0000\u0000\u0000\'(\u0001\u0000\u0000"+
		"\u0000(*\u0001\u0000\u0000\u0000)\'\u0001\u0000\u0000\u0000*+\u0005\""+
		"\u0000\u0000+\n\u0001\u0000\u0000\u0000,.\u0003\r\u0006\u0000-,\u0001"+
		"\u0000\u0000\u0000./\u0001\u0000\u0000\u0000/-\u0001\u0000\u0000\u0000"+
		"/0\u0001\u0000\u0000\u000004\u0001\u0000\u0000\u000013\u0005 \u0000\u0000"+
		"21\u0001\u0000\u0000\u000036\u0001\u0000\u0000\u000042\u0001\u0000\u0000"+
		"\u000045\u0001\u0000\u0000\u000058\u0001\u0000\u0000\u000064\u0001\u0000"+
		"\u0000\u000079\u0003\r\u0006\u000087\u0001\u0000\u0000\u00009:\u0001\u0000"+
		"\u0000\u0000:8\u0001\u0000\u0000\u0000:;\u0001\u0000\u0000\u0000;B\u0001"+
		"\u0000\u0000\u0000<>\u0003\r\u0006\u0000=<\u0001\u0000\u0000\u0000>?\u0001"+
		"\u0000\u0000\u0000?=\u0001\u0000\u0000\u0000?@\u0001\u0000\u0000\u0000"+
		"@B\u0001\u0000\u0000\u0000A-\u0001\u0000\u0000\u0000A=\u0001\u0000\u0000"+
		"\u0000B\f\u0001\u0000\u0000\u0000CD\b\u0004\u0000\u0000D\u000e\u0001\u0000"+
		"\u0000\u0000EH\u0005\\\u0000\u0000FI\u0007\u0005\u0000\u0000GI\u0003\u0011"+
		"\b\u0000HF\u0001\u0000\u0000\u0000HG\u0001\u0000\u0000\u0000I\u0010\u0001"+
		"\u0000\u0000\u0000JK\u0005u\u0000\u0000KL\u0003\u0013\t\u0000LM\u0003"+
		"\u0013\t\u0000MN\u0003\u0013\t\u0000NO\u0003\u0013\t\u0000O\u0012\u0001"+
		"\u0000\u0000\u0000PQ\u0007\u0006\u0000\u0000Q\u0014\u0001\u0000\u0000"+
		"\u0000RT\u0007\u0007\u0000\u0000SR\u0001\u0000\u0000\u0000TU\u0001\u0000"+
		"\u0000\u0000US\u0001\u0000\u0000\u0000UV\u0001\u0000\u0000\u0000VW\u0001"+
		"\u0000\u0000\u0000WX\u0006\n\u0000\u0000X\u0016\u0001\u0000\u0000\u0000"+
		"\n\u0000%\'/4:?AHU\u0001\u0006\u0000\u0000";
	public static final ATN _ATN =
		new ATNDeserializer().deserialize(_serializedATN.toCharArray());
	static {
		_decisionToDFA = new DFA[_ATN.getNumberOfDecisions()];
		for (int i = 0; i < _ATN.getNumberOfDecisions(); i++) {
			_decisionToDFA[i] = new DFA(_ATN.getDecisionState(i), i);
		}
	}
}