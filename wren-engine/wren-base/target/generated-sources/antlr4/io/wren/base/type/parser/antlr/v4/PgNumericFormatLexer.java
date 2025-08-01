// Generated from io/wren/base/type/parser/antlr/v4/PgNumericFormat.g4 by ANTLR 4.13.2
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
public class PgNumericFormatLexer extends Lexer {
	static { RuntimeMetaData.checkVersion("4.13.2", RuntimeMetaData.VERSION); }

	protected static final DFA[] _decisionToDFA;
	protected static final PredictionContextCache _sharedContextCache =
		new PredictionContextCache();
	public static final int
		DIGIT_CAN_DROP=1, DIGIT_CAN_NOT_DROP=2, DECIMAL_POINT=3, GROUP_SEPARATOR=4, 
		PR=5, SIGN_ANCHOR_LOCALE=6, CURRENCY_SYMBOL=7, DECIMAL_POINT_LOCALE=8, 
		GROUP_SEPARATOR_LOCALE=9, MINUS=10, PLUS=11, SIGN=12, ROMAN=13, ORDINAL=14, 
		SHIFT_DIGIT=15, EXPONENT=16, FM=17;
	public static String[] channelNames = {
		"DEFAULT_TOKEN_CHANNEL", "HIDDEN"
	};

	public static String[] modeNames = {
		"DEFAULT_MODE"
	};

	private static String[] makeRuleNames() {
		return new String[] {
			"DIGIT_CAN_DROP", "DIGIT_CAN_NOT_DROP", "DECIMAL_POINT", "GROUP_SEPARATOR", 
			"PR", "SIGN_ANCHOR_LOCALE", "CURRENCY_SYMBOL", "DECIMAL_POINT_LOCALE", 
			"GROUP_SEPARATOR_LOCALE", "MINUS", "PLUS", "SIGN", "ROMAN", "ORDINAL", 
			"SHIFT_DIGIT", "EXPONENT", "FM"
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


	public PgNumericFormatLexer(CharStream input) {
		super(input);
		_interp = new LexerATNSimulator(this,_ATN,_decisionToDFA,_sharedContextCache);
	}

	@Override
	public String getGrammarFileName() { return "PgNumericFormat.g4"; }

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
		"\u0004\u0000\u0011R\u0006\uffff\uffff\u0002\u0000\u0007\u0000\u0002\u0001"+
		"\u0007\u0001\u0002\u0002\u0007\u0002\u0002\u0003\u0007\u0003\u0002\u0004"+
		"\u0007\u0004\u0002\u0005\u0007\u0005\u0002\u0006\u0007\u0006\u0002\u0007"+
		"\u0007\u0007\u0002\b\u0007\b\u0002\t\u0007\t\u0002\n\u0007\n\u0002\u000b"+
		"\u0007\u000b\u0002\f\u0007\f\u0002\r\u0007\r\u0002\u000e\u0007\u000e\u0002"+
		"\u000f\u0007\u000f\u0002\u0010\u0007\u0010\u0001\u0000\u0001\u0000\u0001"+
		"\u0001\u0001\u0001\u0001\u0002\u0001\u0002\u0001\u0003\u0001\u0003\u0001"+
		"\u0004\u0001\u0004\u0001\u0004\u0001\u0005\u0001\u0005\u0001\u0006\u0001"+
		"\u0006\u0001\u0007\u0001\u0007\u0001\b\u0001\b\u0001\t\u0001\t\u0001\t"+
		"\u0001\n\u0001\n\u0001\n\u0001\u000b\u0001\u000b\u0001\u000b\u0001\f\u0001"+
		"\f\u0001\f\u0001\r\u0001\r\u0001\r\u0001\r\u0003\rG\b\r\u0001\u000e\u0001"+
		"\u000e\u0001\u000f\u0001\u000f\u0001\u000f\u0001\u000f\u0001\u000f\u0001"+
		"\u0010\u0001\u0010\u0001\u0010\u0000\u0000\u0011\u0001\u0001\u0003\u0002"+
		"\u0005\u0003\u0007\u0004\t\u0005\u000b\u0006\r\u0007\u000f\b\u0011\t\u0013"+
		"\n\u0015\u000b\u0017\f\u0019\r\u001b\u000e\u001d\u000f\u001f\u0010!\u0011"+
		"\u0001\u0000\u0000R\u0000\u0001\u0001\u0000\u0000\u0000\u0000\u0003\u0001"+
		"\u0000\u0000\u0000\u0000\u0005\u0001\u0000\u0000\u0000\u0000\u0007\u0001"+
		"\u0000\u0000\u0000\u0000\t\u0001\u0000\u0000\u0000\u0000\u000b\u0001\u0000"+
		"\u0000\u0000\u0000\r\u0001\u0000\u0000\u0000\u0000\u000f\u0001\u0000\u0000"+
		"\u0000\u0000\u0011\u0001\u0000\u0000\u0000\u0000\u0013\u0001\u0000\u0000"+
		"\u0000\u0000\u0015\u0001\u0000\u0000\u0000\u0000\u0017\u0001\u0000\u0000"+
		"\u0000\u0000\u0019\u0001\u0000\u0000\u0000\u0000\u001b\u0001\u0000\u0000"+
		"\u0000\u0000\u001d\u0001\u0000\u0000\u0000\u0000\u001f\u0001\u0000\u0000"+
		"\u0000\u0000!\u0001\u0000\u0000\u0000\u0001#\u0001\u0000\u0000\u0000\u0003"+
		"%\u0001\u0000\u0000\u0000\u0005\'\u0001\u0000\u0000\u0000\u0007)\u0001"+
		"\u0000\u0000\u0000\t+\u0001\u0000\u0000\u0000\u000b.\u0001\u0000\u0000"+
		"\u0000\r0\u0001\u0000\u0000\u0000\u000f2\u0001\u0000\u0000\u0000\u0011"+
		"4\u0001\u0000\u0000\u0000\u00136\u0001\u0000\u0000\u0000\u00159\u0001"+
		"\u0000\u0000\u0000\u0017<\u0001\u0000\u0000\u0000\u0019?\u0001\u0000\u0000"+
		"\u0000\u001bF\u0001\u0000\u0000\u0000\u001dH\u0001\u0000\u0000\u0000\u001f"+
		"J\u0001\u0000\u0000\u0000!O\u0001\u0000\u0000\u0000#$\u00059\u0000\u0000"+
		"$\u0002\u0001\u0000\u0000\u0000%&\u00050\u0000\u0000&\u0004\u0001\u0000"+
		"\u0000\u0000\'(\u0005.\u0000\u0000(\u0006\u0001\u0000\u0000\u0000)*\u0005"+
		",\u0000\u0000*\b\u0001\u0000\u0000\u0000+,\u0005P\u0000\u0000,-\u0005"+
		"R\u0000\u0000-\n\u0001\u0000\u0000\u0000./\u0005S\u0000\u0000/\f\u0001"+
		"\u0000\u0000\u000001\u0005L\u0000\u00001\u000e\u0001\u0000\u0000\u0000"+
		"23\u0005D\u0000\u00003\u0010\u0001\u0000\u0000\u000045\u0005G\u0000\u0000"+
		"5\u0012\u0001\u0000\u0000\u000067\u0005M\u0000\u000078\u0005I\u0000\u0000"+
		"8\u0014\u0001\u0000\u0000\u00009:\u0005P\u0000\u0000:;\u0005L\u0000\u0000"+
		";\u0016\u0001\u0000\u0000\u0000<=\u0005S\u0000\u0000=>\u0005G\u0000\u0000"+
		">\u0018\u0001\u0000\u0000\u0000?@\u0005R\u0000\u0000@A\u0005N\u0000\u0000"+
		"A\u001a\u0001\u0000\u0000\u0000BC\u0005T\u0000\u0000CG\u0005H\u0000\u0000"+
		"DE\u0005t\u0000\u0000EG\u0005h\u0000\u0000FB\u0001\u0000\u0000\u0000F"+
		"D\u0001\u0000\u0000\u0000G\u001c\u0001\u0000\u0000\u0000HI\u0005V\u0000"+
		"\u0000I\u001e\u0001\u0000\u0000\u0000JK\u0005E\u0000\u0000KL\u0005E\u0000"+
		"\u0000LM\u0005E\u0000\u0000MN\u0005E\u0000\u0000N \u0001\u0000\u0000\u0000"+
		"OP\u0005F\u0000\u0000PQ\u0005M\u0000\u0000Q\"\u0001\u0000\u0000\u0000"+
		"\u0002\u0000F\u0000";
	public static final ATN _ATN =
		new ATNDeserializer().deserialize(_serializedATN.toCharArray());
	static {
		_decisionToDFA = new DFA[_ATN.getNumberOfDecisions()];
		for (int i = 0; i < _ATN.getNumberOfDecisions(); i++) {
			_decisionToDFA[i] = new DFA(_ATN.getDecisionState(i), i);
		}
	}
}