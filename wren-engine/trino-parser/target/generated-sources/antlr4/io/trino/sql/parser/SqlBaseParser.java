// Generated from io/trino/sql/parser/SqlBase.g4 by ANTLR 4.13.2
package io.trino.sql.parser;
import org.antlr.v4.runtime.atn.*;
import org.antlr.v4.runtime.dfa.DFA;
import org.antlr.v4.runtime.*;
import org.antlr.v4.runtime.misc.*;
import org.antlr.v4.runtime.tree.*;
import java.util.List;
import java.util.Iterator;
import java.util.ArrayList;

@SuppressWarnings({"all", "warnings", "unchecked", "unused", "cast", "CheckReturnValue", "this-escape"})
public class SqlBaseParser extends Parser {
	static { RuntimeMetaData.checkVersion("4.13.2", RuntimeMetaData.VERSION); }

	protected static final DFA[] _decisionToDFA;
	protected static final PredictionContextCache _sharedContextCache =
		new PredictionContextCache();
	public static final int
		T__0=1, T__1=2, T__2=3, T__3=4, T__4=5, T__5=6, T__6=7, T__7=8, T__8=9, 
		T__9=10, T__10=11, T__11=12, T__12=13, T__13=14, T__14=15, T__15=16, T__16=17, 
		T__17=18, T__18=19, T__19=20, T__20=21, ADD=22, ADMIN=23, AFTER=24, ALL=25, 
		ALTER=26, ANALYZE=27, AND=28, ANY=29, ARRAY=30, AS=31, ASC=32, AT=33, 
		AUTHORIZATION=34, BERNOULLI=35, BETWEEN=36, BY=37, CALL=38, CASCADE=39, 
		CASE=40, CAST=41, CATALOGS=42, COLLATE=43, COLUMN=44, COLUMNS=45, COMMENT=46, 
		COMMIT=47, COMMITTED=48, CONSTRAINT=49, COUNT=50, CREATE=51, CROSS=52, 
		CUBE=53, CURRENT=54, CURRENT_CATALOG=55, CURRENT_DATE=56, CURRENT_PATH=57, 
		CURRENT_ROLE=58, CURRENT_SCHEMA=59, CURRENT_TIME=60, CURRENT_TIMESTAMP=61, 
		CURRENT_USER=62, CURSOR=63, DATA=64, DATE=65, DAY=66, DEALLOCATE=67, DECLARE=68, 
		DEFAULT=69, DEFINER=70, DELETE=71, DENY=72, DESC=73, DESCRIBE=74, DEFINE=75, 
		DISTINCT=76, DISTRIBUTED=77, DOUBLE=78, DROP=79, ELSE=80, EMPTY=81, END=82, 
		EPOCH=83, ERROR=84, ESCAPE=85, EXCEPT=86, EXCLUDING=87, EXECUTE=88, EXISTS=89, 
		EXPLAIN=90, EXTRACT=91, FALSE=92, FETCH=93, FILTER=94, FINAL=95, FIRST=96, 
		FOLLOWING=97, FOR=98, FORMAT=99, FROM=100, FULL=101, FUNCTIONS=102, GRANT=103, 
		GRANTED=104, GRANTS=105, GRAPHVIZ=106, GROUP=107, GROUPING=108, GROUPS=109, 
		HAVING=110, HOUR=111, IF=112, IGNORE=113, IMPERSONATE=114, IN=115, INCLUDING=116, 
		INITIAL=117, INNER=118, INPUT=119, INSERT=120, INTERSECT=121, INTERVAL=122, 
		INTO=123, INVOKER=124, IO=125, IS=126, ISOLATION=127, JOIN=128, JSON=129, 
		LAST=130, LATERAL=131, LEFT=132, LEVEL=133, LIKE=134, LIMIT=135, LISTAGG=136, 
		LOCAL=137, LOCALTIME=138, LOCALTIMESTAMP=139, LOGICAL=140, MAP=141, MATCH=142, 
		MATCHED=143, MATCHES=144, MATCH_RECOGNIZE=145, MATERIALIZED=146, MEASURES=147, 
		MERGE=148, MINUTE=149, MONTH=150, NATURAL=151, NEXT=152, NFC=153, NFD=154, 
		NFKC=155, NFKD=156, NO=157, NONE=158, NORMALIZE=159, NOT=160, NULL=161, 
		NULLIF=162, NULLS=163, OFFSET=164, OMIT=165, OF=166, ON=167, ONE=168, 
		ONLY=169, OPERATOR=170, OPTION=171, OR=172, ORDER=173, ORDINALITY=174, 
		OUTER=175, OUTPUT=176, OVER=177, OVERFLOW=178, PARTITION=179, PARTITIONS=180, 
		PAST=181, PATH=182, PATTERN=183, PER=184, PERMUTE=185, POSITION=186, PRECEDING=187, 
		PRECISION=188, PREPARE=189, PRIVILEGES=190, PROPERTIES=191, RANGE=192, 
		READ=193, RECURSIVE=194, REFRESH=195, RENAME=196, REPEATABLE=197, REPLACE=198, 
		RESET=199, RESPECT=200, RESTRICT=201, REVOKE=202, RIGHT=203, ROLE=204, 
		ROLES=205, ROLLBACK=206, ROLLUP=207, ROW=208, ROWS=209, RUNNING=210, SCHEMA=211, 
		SCHEMAS=212, SECOND=213, SECURITY=214, SEEK=215, SELECT=216, SERIALIZABLE=217, 
		SESSION=218, SESSION_USER=219, SET=220, SETS=221, SHOW=222, SOME=223, 
		START=224, STATS=225, SUBSET=226, SUBSTRING=227, SYSTEM=228, TABLE=229, 
		TABLES=230, TABLESAMPLE=231, TEXT=232, THEN=233, TIES=234, TIME=235, TIMESTAMP=236, 
		TO=237, TRANSACTION=238, TRUE=239, TRUNCATE=240, TRY_CAST=241, TYPE=242, 
		UESCAPE=243, UNBOUNDED=244, UNCOMMITTED=245, UNION=246, UNMATCHED=247, 
		UNNEST=248, UPDATE=249, USE=250, USER=251, USING=252, VALIDATE=253, VALUES=254, 
		VERBOSE=255, VERSION=256, VIEW=257, WHEN=258, WHERE=259, WINDOW=260, WITH=261, 
		WITHIN=262, WITHOUT=263, WORK=264, WRITE=265, YEAR=266, ZONE=267, EQ=268, 
		NEQ=269, LT=270, LTE=271, GT=272, GTE=273, PLUS=274, MINUS=275, ASTERISK=276, 
		SLASH=277, PERCENT=278, CONCAT=279, QUESTION_MARK=280, REGEX_MATCH=281, 
		STRING=282, UNICODE_STRING=283, BINARY_LITERAL=284, INTEGER_VALUE=285, 
		DECIMAL_VALUE=286, DOUBLE_VALUE=287, IDENTIFIER=288, DIGIT_IDENTIFIER=289, 
		QUOTED_IDENTIFIER=290, BACKQUOTED_IDENTIFIER=291, SIMPLE_COMMENT=292, 
		BRACKETED_COMMENT=293, WS=294, UNRECOGNIZED=295, PG_CAST=296, ESCAPED_STRING=297, 
		DELIMITER=298;
	public static final int
		RULE_singleStatement = 0, RULE_standaloneExpression = 1, RULE_standalonePathSpecification = 2, 
		RULE_standaloneType = 3, RULE_standaloneRowPattern = 4, RULE_statement = 5, 
		RULE_query = 6, RULE_with = 7, RULE_tableElement = 8, RULE_columnDefinition = 9, 
		RULE_likeClause = 10, RULE_properties = 11, RULE_propertyAssignments = 12, 
		RULE_property = 13, RULE_propertyValue = 14, RULE_queryNoWith = 15, RULE_pgCast = 16, 
		RULE_limitRowCount = 17, RULE_rowCount = 18, RULE_queryTerm = 19, RULE_queryPrimary = 20, 
		RULE_sortItem = 21, RULE_querySpecification = 22, RULE_groupBy = 23, RULE_groupingElement = 24, 
		RULE_groupingSet = 25, RULE_windowDefinition = 26, RULE_windowSpecification = 27, 
		RULE_namedQuery = 28, RULE_setQuantifier = 29, RULE_selectItem = 30, RULE_relation = 31, 
		RULE_joinType = 32, RULE_joinCriteria = 33, RULE_sampledRelation = 34, 
		RULE_sampleType = 35, RULE_listAggOverflowBehavior = 36, RULE_listaggCountIndication = 37, 
		RULE_patternRecognition = 38, RULE_measureDefinition = 39, RULE_rowsPerMatch = 40, 
		RULE_emptyMatchHandling = 41, RULE_skipTo = 42, RULE_subsetDefinition = 43, 
		RULE_variableDefinition = 44, RULE_aliasedRelation = 45, RULE_columnAliases = 46, 
		RULE_relationPrimary = 47, RULE_expression = 48, RULE_booleanExpression = 49, 
		RULE_predicate = 50, RULE_functionExpression = 51, RULE_valueExpression = 52, 
		RULE_primaryExpression = 53, RULE_processingMode = 54, RULE_nullTreatment = 55, 
		RULE_string = 56, RULE_timeZoneSpecifier = 57, RULE_comparisonOperator = 58, 
		RULE_comparisonQuantifier = 59, RULE_booleanValue = 60, RULE_interval = 61, 
		RULE_intervalField = 62, RULE_normalForm = 63, RULE_type = 64, RULE_rowField = 65, 
		RULE_typeParameter = 66, RULE_whenClause = 67, RULE_filter = 68, RULE_mergeCase = 69, 
		RULE_over = 70, RULE_windowFrame = 71, RULE_frameExtent = 72, RULE_frameBound = 73, 
		RULE_rowPattern = 74, RULE_patternPrimary = 75, RULE_patternQuantifier = 76, 
		RULE_updateAssignment = 77, RULE_explainOption = 78, RULE_transactionMode = 79, 
		RULE_levelOfIsolation = 80, RULE_callArgument = 81, RULE_pathElement = 82, 
		RULE_pathSpecification = 83, RULE_privilege = 84, RULE_qualifiedName = 85, 
		RULE_queryPeriod = 86, RULE_rangeType = 87, RULE_grantor = 88, RULE_principal = 89, 
		RULE_roles = 90, RULE_identifier = 91, RULE_number = 92, RULE_quotedRegexMatch = 93, 
		RULE_collateClause = 94, RULE_nonReserved = 95;
	private static String[] makeRuleNames() {
		return new String[] {
			"singleStatement", "standaloneExpression", "standalonePathSpecification", 
			"standaloneType", "standaloneRowPattern", "statement", "query", "with", 
			"tableElement", "columnDefinition", "likeClause", "properties", "propertyAssignments", 
			"property", "propertyValue", "queryNoWith", "pgCast", "limitRowCount", 
			"rowCount", "queryTerm", "queryPrimary", "sortItem", "querySpecification", 
			"groupBy", "groupingElement", "groupingSet", "windowDefinition", "windowSpecification", 
			"namedQuery", "setQuantifier", "selectItem", "relation", "joinType", 
			"joinCriteria", "sampledRelation", "sampleType", "listAggOverflowBehavior", 
			"listaggCountIndication", "patternRecognition", "measureDefinition", 
			"rowsPerMatch", "emptyMatchHandling", "skipTo", "subsetDefinition", "variableDefinition", 
			"aliasedRelation", "columnAliases", "relationPrimary", "expression", 
			"booleanExpression", "predicate", "functionExpression", "valueExpression", 
			"primaryExpression", "processingMode", "nullTreatment", "string", "timeZoneSpecifier", 
			"comparisonOperator", "comparisonQuantifier", "booleanValue", "interval", 
			"intervalField", "normalForm", "type", "rowField", "typeParameter", "whenClause", 
			"filter", "mergeCase", "over", "windowFrame", "frameExtent", "frameBound", 
			"rowPattern", "patternPrimary", "patternQuantifier", "updateAssignment", 
			"explainOption", "transactionMode", "levelOfIsolation", "callArgument", 
			"pathElement", "pathSpecification", "privilege", "qualifiedName", "queryPeriod", 
			"rangeType", "grantor", "principal", "roles", "identifier", "number", 
			"quotedRegexMatch", "collateClause", "nonReserved"
		};
	}
	public static final String[] ruleNames = makeRuleNames();

	private static String[] makeLiteralNames() {
		return new String[] {
			null, "'.'", "'('", "')'", "','", "'BINARY'", "'ASENSITIVE'", "'INSENSITIVE'", 
			"'SCROLL'", "'HOLD'", "'SKIP'", "'->'", "'['", "']'", "'|'", "'^'", "'$'", 
			"'{-'", "'-}'", "'{'", "'}'", "'=>'", "'ADD'", "'ADMIN'", "'AFTER'", 
			"'ALL'", "'ALTER'", "'ANALYZE'", "'AND'", "'ANY'", "'ARRAY'", "'AS'", 
			"'ASC'", "'AT'", "'AUTHORIZATION'", "'BERNOULLI'", "'BETWEEN'", "'BY'", 
			"'CALL'", "'CASCADE'", "'CASE'", "'CAST'", "'CATALOGS'", "'COLLATE'", 
			"'COLUMN'", "'COLUMNS'", "'COMMENT'", "'COMMIT'", "'COMMITTED'", "'CONSTRAINT'", 
			"'COUNT'", "'CREATE'", "'CROSS'", "'CUBE'", "'CURRENT'", "'CURRENT_CATALOG'", 
			"'CURRENT_DATE'", "'CURRENT_PATH'", "'CURRENT_ROLE'", "'CURRENT_SCHEMA'", 
			"'CURRENT_TIME'", "'CURRENT_TIMESTAMP'", "'CURRENT_USER'", "'CURSOR'", 
			"'DATA'", "'DATE'", "'DAY'", "'DEALLOCATE'", "'DECLARE'", "'DEFAULT'", 
			"'DEFINER'", "'DELETE'", "'DENY'", "'DESC'", "'DESCRIBE'", "'DEFINE'", 
			"'DISTINCT'", "'DISTRIBUTED'", "'DOUBLE'", "'DROP'", "'ELSE'", "'EMPTY'", 
			"'END'", "'EPOCH'", "'ERROR'", "'ESCAPE'", "'EXCEPT'", "'EXCLUDING'", 
			"'EXECUTE'", "'EXISTS'", "'EXPLAIN'", "'EXTRACT'", "'FALSE'", "'FETCH'", 
			"'FILTER'", "'FINAL'", "'FIRST'", "'FOLLOWING'", "'FOR'", "'FORMAT'", 
			"'FROM'", "'FULL'", "'FUNCTIONS'", "'GRANT'", "'GRANTED'", "'GRANTS'", 
			"'GRAPHVIZ'", "'GROUP'", "'GROUPING'", "'GROUPS'", "'HAVING'", "'HOUR'", 
			"'IF'", "'IGNORE'", "'IMPERSONATE'", "'IN'", "'INCLUDING'", "'INITIAL'", 
			"'INNER'", "'INPUT'", "'INSERT'", "'INTERSECT'", "'INTERVAL'", "'INTO'", 
			"'INVOKER'", "'IO'", "'IS'", "'ISOLATION'", "'JOIN'", "'JSON'", "'LAST'", 
			"'LATERAL'", "'LEFT'", "'LEVEL'", null, "'LIMIT'", "'LISTAGG'", "'LOCAL'", 
			"'LOCALTIME'", "'LOCALTIMESTAMP'", "'LOGICAL'", "'MAP'", "'MATCH'", "'MATCHED'", 
			"'MATCHES'", "'MATCH_RECOGNIZE'", "'MATERIALIZED'", "'MEASURES'", "'MERGE'", 
			"'MINUTE'", "'MONTH'", "'NATURAL'", "'NEXT'", "'NFC'", "'NFD'", "'NFKC'", 
			"'NFKD'", "'NO'", "'NONE'", "'NORMALIZE'", null, "'NULL'", "'NULLIF'", 
			"'NULLS'", "'OFFSET'", "'OMIT'", "'OF'", "'ON'", "'ONE'", "'ONLY'", "'OPERATOR'", 
			"'OPTION'", "'OR'", "'ORDER'", "'ORDINALITY'", "'OUTER'", "'OUTPUT'", 
			"'OVER'", "'OVERFLOW'", "'PARTITION'", "'PARTITIONS'", "'PAST'", "'PATH'", 
			"'PATTERN'", "'PER'", "'PERMUTE'", "'POSITION'", "'PRECEDING'", "'PRECISION'", 
			"'PREPARE'", "'PRIVILEGES'", "'PROPERTIES'", "'RANGE'", "'READ'", "'RECURSIVE'", 
			"'REFRESH'", "'RENAME'", "'REPEATABLE'", "'REPLACE'", "'RESET'", "'RESPECT'", 
			"'RESTRICT'", "'REVOKE'", "'RIGHT'", "'ROLE'", "'ROLES'", "'ROLLBACK'", 
			"'ROLLUP'", "'ROW'", "'ROWS'", "'RUNNING'", "'SCHEMA'", "'SCHEMAS'", 
			"'SECOND'", "'SECURITY'", "'SEEK'", "'SELECT'", "'SERIALIZABLE'", "'SESSION'", 
			"'SESSION_USER'", "'SET'", "'SETS'", "'SHOW'", "'SOME'", "'START'", "'STATS'", 
			"'SUBSET'", "'SUBSTRING'", "'SYSTEM'", "'TABLE'", "'TABLES'", "'TABLESAMPLE'", 
			"'TEXT'", "'THEN'", "'TIES'", "'TIME'", "'TIMESTAMP'", "'TO'", "'TRANSACTION'", 
			"'TRUE'", "'TRUNCATE'", "'TRY_CAST'", "'TYPE'", "'UESCAPE'", "'UNBOUNDED'", 
			"'UNCOMMITTED'", "'UNION'", "'UNMATCHED'", "'UNNEST'", "'UPDATE'", "'USE'", 
			"'USER'", "'USING'", "'VALIDATE'", "'VALUES'", "'VERBOSE'", "'VERSION'", 
			"'VIEW'", "'WHEN'", "'WHERE'", "'WINDOW'", "'WITH'", "'WITHIN'", "'WITHOUT'", 
			"'WORK'", "'WRITE'", "'YEAR'", "'ZONE'", "'='", null, "'<'", "'<='", 
			"'>'", "'>='", "'+'", "'-'", "'*'", "'/'", "'%'", "'||'", "'?'", "'~'", 
			null, null, null, null, null, null, null, null, null, null, null, null, 
			null, null, "'::'"
		};
	}
	private static final String[] _LITERAL_NAMES = makeLiteralNames();
	private static String[] makeSymbolicNames() {
		return new String[] {
			null, null, null, null, null, null, null, null, null, null, null, null, 
			null, null, null, null, null, null, null, null, null, null, "ADD", "ADMIN", 
			"AFTER", "ALL", "ALTER", "ANALYZE", "AND", "ANY", "ARRAY", "AS", "ASC", 
			"AT", "AUTHORIZATION", "BERNOULLI", "BETWEEN", "BY", "CALL", "CASCADE", 
			"CASE", "CAST", "CATALOGS", "COLLATE", "COLUMN", "COLUMNS", "COMMENT", 
			"COMMIT", "COMMITTED", "CONSTRAINT", "COUNT", "CREATE", "CROSS", "CUBE", 
			"CURRENT", "CURRENT_CATALOG", "CURRENT_DATE", "CURRENT_PATH", "CURRENT_ROLE", 
			"CURRENT_SCHEMA", "CURRENT_TIME", "CURRENT_TIMESTAMP", "CURRENT_USER", 
			"CURSOR", "DATA", "DATE", "DAY", "DEALLOCATE", "DECLARE", "DEFAULT", 
			"DEFINER", "DELETE", "DENY", "DESC", "DESCRIBE", "DEFINE", "DISTINCT", 
			"DISTRIBUTED", "DOUBLE", "DROP", "ELSE", "EMPTY", "END", "EPOCH", "ERROR", 
			"ESCAPE", "EXCEPT", "EXCLUDING", "EXECUTE", "EXISTS", "EXPLAIN", "EXTRACT", 
			"FALSE", "FETCH", "FILTER", "FINAL", "FIRST", "FOLLOWING", "FOR", "FORMAT", 
			"FROM", "FULL", "FUNCTIONS", "GRANT", "GRANTED", "GRANTS", "GRAPHVIZ", 
			"GROUP", "GROUPING", "GROUPS", "HAVING", "HOUR", "IF", "IGNORE", "IMPERSONATE", 
			"IN", "INCLUDING", "INITIAL", "INNER", "INPUT", "INSERT", "INTERSECT", 
			"INTERVAL", "INTO", "INVOKER", "IO", "IS", "ISOLATION", "JOIN", "JSON", 
			"LAST", "LATERAL", "LEFT", "LEVEL", "LIKE", "LIMIT", "LISTAGG", "LOCAL", 
			"LOCALTIME", "LOCALTIMESTAMP", "LOGICAL", "MAP", "MATCH", "MATCHED", 
			"MATCHES", "MATCH_RECOGNIZE", "MATERIALIZED", "MEASURES", "MERGE", "MINUTE", 
			"MONTH", "NATURAL", "NEXT", "NFC", "NFD", "NFKC", "NFKD", "NO", "NONE", 
			"NORMALIZE", "NOT", "NULL", "NULLIF", "NULLS", "OFFSET", "OMIT", "OF", 
			"ON", "ONE", "ONLY", "OPERATOR", "OPTION", "OR", "ORDER", "ORDINALITY", 
			"OUTER", "OUTPUT", "OVER", "OVERFLOW", "PARTITION", "PARTITIONS", "PAST", 
			"PATH", "PATTERN", "PER", "PERMUTE", "POSITION", "PRECEDING", "PRECISION", 
			"PREPARE", "PRIVILEGES", "PROPERTIES", "RANGE", "READ", "RECURSIVE", 
			"REFRESH", "RENAME", "REPEATABLE", "REPLACE", "RESET", "RESPECT", "RESTRICT", 
			"REVOKE", "RIGHT", "ROLE", "ROLES", "ROLLBACK", "ROLLUP", "ROW", "ROWS", 
			"RUNNING", "SCHEMA", "SCHEMAS", "SECOND", "SECURITY", "SEEK", "SELECT", 
			"SERIALIZABLE", "SESSION", "SESSION_USER", "SET", "SETS", "SHOW", "SOME", 
			"START", "STATS", "SUBSET", "SUBSTRING", "SYSTEM", "TABLE", "TABLES", 
			"TABLESAMPLE", "TEXT", "THEN", "TIES", "TIME", "TIMESTAMP", "TO", "TRANSACTION", 
			"TRUE", "TRUNCATE", "TRY_CAST", "TYPE", "UESCAPE", "UNBOUNDED", "UNCOMMITTED", 
			"UNION", "UNMATCHED", "UNNEST", "UPDATE", "USE", "USER", "USING", "VALIDATE", 
			"VALUES", "VERBOSE", "VERSION", "VIEW", "WHEN", "WHERE", "WINDOW", "WITH", 
			"WITHIN", "WITHOUT", "WORK", "WRITE", "YEAR", "ZONE", "EQ", "NEQ", "LT", 
			"LTE", "GT", "GTE", "PLUS", "MINUS", "ASTERISK", "SLASH", "PERCENT", 
			"CONCAT", "QUESTION_MARK", "REGEX_MATCH", "STRING", "UNICODE_STRING", 
			"BINARY_LITERAL", "INTEGER_VALUE", "DECIMAL_VALUE", "DOUBLE_VALUE", "IDENTIFIER", 
			"DIGIT_IDENTIFIER", "QUOTED_IDENTIFIER", "BACKQUOTED_IDENTIFIER", "SIMPLE_COMMENT", 
			"BRACKETED_COMMENT", "WS", "UNRECOGNIZED", "PG_CAST", "ESCAPED_STRING", 
			"DELIMITER"
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
	public String getGrammarFileName() { return "SqlBase.g4"; }

	@Override
	public String[] getRuleNames() { return ruleNames; }

	@Override
	public String getSerializedATN() { return _serializedATN; }

	@Override
	public ATN getATN() { return _ATN; }

	public SqlBaseParser(TokenStream input) {
		super(input);
		_interp = new ParserATNSimulator(this,_ATN,_decisionToDFA,_sharedContextCache);
	}

	@SuppressWarnings("CheckReturnValue")
	public static class SingleStatementContext extends ParserRuleContext {
		public StatementContext statement() {
			return getRuleContext(StatementContext.class,0);
		}
		public TerminalNode EOF() { return getToken(SqlBaseParser.EOF, 0); }
		public SingleStatementContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_singleStatement; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterSingleStatement(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitSingleStatement(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitSingleStatement(this);
			else return visitor.visitChildren(this);
		}
	}

	public final SingleStatementContext singleStatement() throws RecognitionException {
		SingleStatementContext _localctx = new SingleStatementContext(_ctx, getState());
		enterRule(_localctx, 0, RULE_singleStatement);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(192);
			statement();
			setState(193);
			match(EOF);
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
	public static class StandaloneExpressionContext extends ParserRuleContext {
		public ExpressionContext expression() {
			return getRuleContext(ExpressionContext.class,0);
		}
		public TerminalNode EOF() { return getToken(SqlBaseParser.EOF, 0); }
		public StandaloneExpressionContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_standaloneExpression; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterStandaloneExpression(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitStandaloneExpression(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitStandaloneExpression(this);
			else return visitor.visitChildren(this);
		}
	}

	public final StandaloneExpressionContext standaloneExpression() throws RecognitionException {
		StandaloneExpressionContext _localctx = new StandaloneExpressionContext(_ctx, getState());
		enterRule(_localctx, 2, RULE_standaloneExpression);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(195);
			expression();
			setState(196);
			match(EOF);
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
	public static class StandalonePathSpecificationContext extends ParserRuleContext {
		public PathSpecificationContext pathSpecification() {
			return getRuleContext(PathSpecificationContext.class,0);
		}
		public TerminalNode EOF() { return getToken(SqlBaseParser.EOF, 0); }
		public StandalonePathSpecificationContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_standalonePathSpecification; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterStandalonePathSpecification(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitStandalonePathSpecification(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitStandalonePathSpecification(this);
			else return visitor.visitChildren(this);
		}
	}

	public final StandalonePathSpecificationContext standalonePathSpecification() throws RecognitionException {
		StandalonePathSpecificationContext _localctx = new StandalonePathSpecificationContext(_ctx, getState());
		enterRule(_localctx, 4, RULE_standalonePathSpecification);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(198);
			pathSpecification();
			setState(199);
			match(EOF);
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
	public static class StandaloneTypeContext extends ParserRuleContext {
		public TypeContext type() {
			return getRuleContext(TypeContext.class,0);
		}
		public TerminalNode EOF() { return getToken(SqlBaseParser.EOF, 0); }
		public StandaloneTypeContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_standaloneType; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterStandaloneType(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitStandaloneType(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitStandaloneType(this);
			else return visitor.visitChildren(this);
		}
	}

	public final StandaloneTypeContext standaloneType() throws RecognitionException {
		StandaloneTypeContext _localctx = new StandaloneTypeContext(_ctx, getState());
		enterRule(_localctx, 6, RULE_standaloneType);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(201);
			type(0);
			setState(202);
			match(EOF);
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
	public static class StandaloneRowPatternContext extends ParserRuleContext {
		public RowPatternContext rowPattern() {
			return getRuleContext(RowPatternContext.class,0);
		}
		public TerminalNode EOF() { return getToken(SqlBaseParser.EOF, 0); }
		public StandaloneRowPatternContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_standaloneRowPattern; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterStandaloneRowPattern(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitStandaloneRowPattern(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitStandaloneRowPattern(this);
			else return visitor.visitChildren(this);
		}
	}

	public final StandaloneRowPatternContext standaloneRowPattern() throws RecognitionException {
		StandaloneRowPatternContext _localctx = new StandaloneRowPatternContext(_ctx, getState());
		enterRule(_localctx, 8, RULE_standaloneRowPattern);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(204);
			rowPattern(0);
			setState(205);
			match(EOF);
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
	public static class StatementContext extends ParserRuleContext {
		public StatementContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_statement; }
	 
		public StatementContext() { }
		public void copyFrom(StatementContext ctx) {
			super.copyFrom(ctx);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class ExplainContext extends StatementContext {
		public TerminalNode EXPLAIN() { return getToken(SqlBaseParser.EXPLAIN, 0); }
		public StatementContext statement() {
			return getRuleContext(StatementContext.class,0);
		}
		public List<ExplainOptionContext> explainOption() {
			return getRuleContexts(ExplainOptionContext.class);
		}
		public ExplainOptionContext explainOption(int i) {
			return getRuleContext(ExplainOptionContext.class,i);
		}
		public ExplainContext(StatementContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterExplain(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitExplain(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitExplain(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class PrepareContext extends StatementContext {
		public TerminalNode PREPARE() { return getToken(SqlBaseParser.PREPARE, 0); }
		public IdentifierContext identifier() {
			return getRuleContext(IdentifierContext.class,0);
		}
		public TerminalNode FROM() { return getToken(SqlBaseParser.FROM, 0); }
		public StatementContext statement() {
			return getRuleContext(StatementContext.class,0);
		}
		public PrepareContext(StatementContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterPrepare(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitPrepare(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitPrepare(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class FetchCursorContext extends StatementContext {
		public Token row;
		public IdentifierContext cursor;
		public TerminalNode FETCH() { return getToken(SqlBaseParser.FETCH, 0); }
		public TerminalNode INTEGER_VALUE() { return getToken(SqlBaseParser.INTEGER_VALUE, 0); }
		public TerminalNode FROM() { return getToken(SqlBaseParser.FROM, 0); }
		public TerminalNode IN() { return getToken(SqlBaseParser.IN, 0); }
		public IdentifierContext identifier() {
			return getRuleContext(IdentifierContext.class,0);
		}
		public FetchCursorContext(StatementContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterFetchCursor(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitFetchCursor(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitFetchCursor(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class DropMaterializedViewContext extends StatementContext {
		public TerminalNode DROP() { return getToken(SqlBaseParser.DROP, 0); }
		public TerminalNode MATERIALIZED() { return getToken(SqlBaseParser.MATERIALIZED, 0); }
		public TerminalNode VIEW() { return getToken(SqlBaseParser.VIEW, 0); }
		public QualifiedNameContext qualifiedName() {
			return getRuleContext(QualifiedNameContext.class,0);
		}
		public TerminalNode IF() { return getToken(SqlBaseParser.IF, 0); }
		public TerminalNode EXISTS() { return getToken(SqlBaseParser.EXISTS, 0); }
		public DropMaterializedViewContext(StatementContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterDropMaterializedView(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitDropMaterializedView(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitDropMaterializedView(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class SetMaterializedViewPropertiesContext extends StatementContext {
		public TerminalNode ALTER() { return getToken(SqlBaseParser.ALTER, 0); }
		public TerminalNode MATERIALIZED() { return getToken(SqlBaseParser.MATERIALIZED, 0); }
		public TerminalNode VIEW() { return getToken(SqlBaseParser.VIEW, 0); }
		public QualifiedNameContext qualifiedName() {
			return getRuleContext(QualifiedNameContext.class,0);
		}
		public TerminalNode SET() { return getToken(SqlBaseParser.SET, 0); }
		public TerminalNode PROPERTIES() { return getToken(SqlBaseParser.PROPERTIES, 0); }
		public PropertyAssignmentsContext propertyAssignments() {
			return getRuleContext(PropertyAssignmentsContext.class,0);
		}
		public SetMaterializedViewPropertiesContext(StatementContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterSetMaterializedViewProperties(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitSetMaterializedViewProperties(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitSetMaterializedViewProperties(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class UseContext extends StatementContext {
		public IdentifierContext schema;
		public IdentifierContext catalog;
		public TerminalNode USE() { return getToken(SqlBaseParser.USE, 0); }
		public List<IdentifierContext> identifier() {
			return getRuleContexts(IdentifierContext.class);
		}
		public IdentifierContext identifier(int i) {
			return getRuleContext(IdentifierContext.class,i);
		}
		public UseContext(StatementContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterUse(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitUse(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitUse(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class DeallocateContext extends StatementContext {
		public TerminalNode DEALLOCATE() { return getToken(SqlBaseParser.DEALLOCATE, 0); }
		public TerminalNode PREPARE() { return getToken(SqlBaseParser.PREPARE, 0); }
		public IdentifierContext identifier() {
			return getRuleContext(IdentifierContext.class,0);
		}
		public DeallocateContext(StatementContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterDeallocate(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitDeallocate(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitDeallocate(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class RenameTableContext extends StatementContext {
		public QualifiedNameContext from;
		public QualifiedNameContext to;
		public TerminalNode ALTER() { return getToken(SqlBaseParser.ALTER, 0); }
		public TerminalNode TABLE() { return getToken(SqlBaseParser.TABLE, 0); }
		public TerminalNode RENAME() { return getToken(SqlBaseParser.RENAME, 0); }
		public TerminalNode TO() { return getToken(SqlBaseParser.TO, 0); }
		public List<QualifiedNameContext> qualifiedName() {
			return getRuleContexts(QualifiedNameContext.class);
		}
		public QualifiedNameContext qualifiedName(int i) {
			return getRuleContext(QualifiedNameContext.class,i);
		}
		public TerminalNode IF() { return getToken(SqlBaseParser.IF, 0); }
		public TerminalNode EXISTS() { return getToken(SqlBaseParser.EXISTS, 0); }
		public RenameTableContext(StatementContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterRenameTable(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitRenameTable(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitRenameTable(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class CommitContext extends StatementContext {
		public TerminalNode COMMIT() { return getToken(SqlBaseParser.COMMIT, 0); }
		public TerminalNode WORK() { return getToken(SqlBaseParser.WORK, 0); }
		public CommitContext(StatementContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterCommit(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitCommit(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitCommit(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class CreateRoleContext extends StatementContext {
		public IdentifierContext name;
		public IdentifierContext catalog;
		public TerminalNode CREATE() { return getToken(SqlBaseParser.CREATE, 0); }
		public TerminalNode ROLE() { return getToken(SqlBaseParser.ROLE, 0); }
		public List<IdentifierContext> identifier() {
			return getRuleContexts(IdentifierContext.class);
		}
		public IdentifierContext identifier(int i) {
			return getRuleContext(IdentifierContext.class,i);
		}
		public TerminalNode WITH() { return getToken(SqlBaseParser.WITH, 0); }
		public TerminalNode ADMIN() { return getToken(SqlBaseParser.ADMIN, 0); }
		public GrantorContext grantor() {
			return getRuleContext(GrantorContext.class,0);
		}
		public TerminalNode IN() { return getToken(SqlBaseParser.IN, 0); }
		public CreateRoleContext(StatementContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterCreateRole(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitCreateRole(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitCreateRole(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class DropColumnContext extends StatementContext {
		public QualifiedNameContext tableName;
		public QualifiedNameContext column;
		public TerminalNode ALTER() { return getToken(SqlBaseParser.ALTER, 0); }
		public TerminalNode TABLE() { return getToken(SqlBaseParser.TABLE, 0); }
		public TerminalNode DROP() { return getToken(SqlBaseParser.DROP, 0); }
		public TerminalNode COLUMN() { return getToken(SqlBaseParser.COLUMN, 0); }
		public List<QualifiedNameContext> qualifiedName() {
			return getRuleContexts(QualifiedNameContext.class);
		}
		public QualifiedNameContext qualifiedName(int i) {
			return getRuleContext(QualifiedNameContext.class,i);
		}
		public List<TerminalNode> IF() { return getTokens(SqlBaseParser.IF); }
		public TerminalNode IF(int i) {
			return getToken(SqlBaseParser.IF, i);
		}
		public List<TerminalNode> EXISTS() { return getTokens(SqlBaseParser.EXISTS); }
		public TerminalNode EXISTS(int i) {
			return getToken(SqlBaseParser.EXISTS, i);
		}
		public DropColumnContext(StatementContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterDropColumn(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitDropColumn(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitDropColumn(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class DropViewContext extends StatementContext {
		public TerminalNode DROP() { return getToken(SqlBaseParser.DROP, 0); }
		public TerminalNode VIEW() { return getToken(SqlBaseParser.VIEW, 0); }
		public QualifiedNameContext qualifiedName() {
			return getRuleContext(QualifiedNameContext.class,0);
		}
		public TerminalNode IF() { return getToken(SqlBaseParser.IF, 0); }
		public TerminalNode EXISTS() { return getToken(SqlBaseParser.EXISTS, 0); }
		public DropViewContext(StatementContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterDropView(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitDropView(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitDropView(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class ShowTablesContext extends StatementContext {
		public StringContext pattern;
		public StringContext escape;
		public TerminalNode SHOW() { return getToken(SqlBaseParser.SHOW, 0); }
		public TerminalNode TABLES() { return getToken(SqlBaseParser.TABLES, 0); }
		public QualifiedNameContext qualifiedName() {
			return getRuleContext(QualifiedNameContext.class,0);
		}
		public TerminalNode LIKE() { return getToken(SqlBaseParser.LIKE, 0); }
		public TerminalNode FROM() { return getToken(SqlBaseParser.FROM, 0); }
		public TerminalNode IN() { return getToken(SqlBaseParser.IN, 0); }
		public List<StringContext> string() {
			return getRuleContexts(StringContext.class);
		}
		public StringContext string(int i) {
			return getRuleContext(StringContext.class,i);
		}
		public TerminalNode ESCAPE() { return getToken(SqlBaseParser.ESCAPE, 0); }
		public ShowTablesContext(StatementContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterShowTables(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitShowTables(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitShowTables(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class SetViewAuthorizationContext extends StatementContext {
		public QualifiedNameContext from;
		public TerminalNode ALTER() { return getToken(SqlBaseParser.ALTER, 0); }
		public TerminalNode VIEW() { return getToken(SqlBaseParser.VIEW, 0); }
		public TerminalNode SET() { return getToken(SqlBaseParser.SET, 0); }
		public TerminalNode AUTHORIZATION() { return getToken(SqlBaseParser.AUTHORIZATION, 0); }
		public PrincipalContext principal() {
			return getRuleContext(PrincipalContext.class,0);
		}
		public QualifiedNameContext qualifiedName() {
			return getRuleContext(QualifiedNameContext.class,0);
		}
		public SetViewAuthorizationContext(StatementContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterSetViewAuthorization(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitSetViewAuthorization(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitSetViewAuthorization(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class ShowCatalogsContext extends StatementContext {
		public StringContext pattern;
		public StringContext escape;
		public TerminalNode SHOW() { return getToken(SqlBaseParser.SHOW, 0); }
		public TerminalNode CATALOGS() { return getToken(SqlBaseParser.CATALOGS, 0); }
		public TerminalNode LIKE() { return getToken(SqlBaseParser.LIKE, 0); }
		public List<StringContext> string() {
			return getRuleContexts(StringContext.class);
		}
		public StringContext string(int i) {
			return getRuleContext(StringContext.class,i);
		}
		public TerminalNode ESCAPE() { return getToken(SqlBaseParser.ESCAPE, 0); }
		public ShowCatalogsContext(StatementContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterShowCatalogs(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitShowCatalogs(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitShowCatalogs(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class ShowRolesContext extends StatementContext {
		public TerminalNode SHOW() { return getToken(SqlBaseParser.SHOW, 0); }
		public TerminalNode ROLES() { return getToken(SqlBaseParser.ROLES, 0); }
		public TerminalNode CURRENT() { return getToken(SqlBaseParser.CURRENT, 0); }
		public IdentifierContext identifier() {
			return getRuleContext(IdentifierContext.class,0);
		}
		public TerminalNode FROM() { return getToken(SqlBaseParser.FROM, 0); }
		public TerminalNode IN() { return getToken(SqlBaseParser.IN, 0); }
		public ShowRolesContext(StatementContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterShowRoles(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitShowRoles(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitShowRoles(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class MergeContext extends StatementContext {
		public TerminalNode MERGE() { return getToken(SqlBaseParser.MERGE, 0); }
		public TerminalNode INTO() { return getToken(SqlBaseParser.INTO, 0); }
		public QualifiedNameContext qualifiedName() {
			return getRuleContext(QualifiedNameContext.class,0);
		}
		public TerminalNode USING() { return getToken(SqlBaseParser.USING, 0); }
		public RelationContext relation() {
			return getRuleContext(RelationContext.class,0);
		}
		public TerminalNode ON() { return getToken(SqlBaseParser.ON, 0); }
		public ExpressionContext expression() {
			return getRuleContext(ExpressionContext.class,0);
		}
		public IdentifierContext identifier() {
			return getRuleContext(IdentifierContext.class,0);
		}
		public List<MergeCaseContext> mergeCase() {
			return getRuleContexts(MergeCaseContext.class);
		}
		public MergeCaseContext mergeCase(int i) {
			return getRuleContext(MergeCaseContext.class,i);
		}
		public TerminalNode AS() { return getToken(SqlBaseParser.AS, 0); }
		public MergeContext(StatementContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterMerge(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitMerge(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitMerge(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class RenameColumnContext extends StatementContext {
		public QualifiedNameContext tableName;
		public IdentifierContext from;
		public IdentifierContext to;
		public TerminalNode ALTER() { return getToken(SqlBaseParser.ALTER, 0); }
		public TerminalNode TABLE() { return getToken(SqlBaseParser.TABLE, 0); }
		public TerminalNode RENAME() { return getToken(SqlBaseParser.RENAME, 0); }
		public TerminalNode COLUMN() { return getToken(SqlBaseParser.COLUMN, 0); }
		public TerminalNode TO() { return getToken(SqlBaseParser.TO, 0); }
		public QualifiedNameContext qualifiedName() {
			return getRuleContext(QualifiedNameContext.class,0);
		}
		public List<IdentifierContext> identifier() {
			return getRuleContexts(IdentifierContext.class);
		}
		public IdentifierContext identifier(int i) {
			return getRuleContext(IdentifierContext.class,i);
		}
		public List<TerminalNode> IF() { return getTokens(SqlBaseParser.IF); }
		public TerminalNode IF(int i) {
			return getToken(SqlBaseParser.IF, i);
		}
		public List<TerminalNode> EXISTS() { return getTokens(SqlBaseParser.EXISTS); }
		public TerminalNode EXISTS(int i) {
			return getToken(SqlBaseParser.EXISTS, i);
		}
		public RenameColumnContext(StatementContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterRenameColumn(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitRenameColumn(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitRenameColumn(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class CommentColumnContext extends StatementContext {
		public TerminalNode COMMENT() { return getToken(SqlBaseParser.COMMENT, 0); }
		public TerminalNode ON() { return getToken(SqlBaseParser.ON, 0); }
		public TerminalNode COLUMN() { return getToken(SqlBaseParser.COLUMN, 0); }
		public QualifiedNameContext qualifiedName() {
			return getRuleContext(QualifiedNameContext.class,0);
		}
		public TerminalNode IS() { return getToken(SqlBaseParser.IS, 0); }
		public StringContext string() {
			return getRuleContext(StringContext.class,0);
		}
		public TerminalNode NULL() { return getToken(SqlBaseParser.NULL, 0); }
		public CommentColumnContext(StatementContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterCommentColumn(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitCommentColumn(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitCommentColumn(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class ImpersonateUserContext extends StatementContext {
		public TerminalNode IMPERSONATE() { return getToken(SqlBaseParser.IMPERSONATE, 0); }
		public ExpressionContext expression() {
			return getRuleContext(ExpressionContext.class,0);
		}
		public ImpersonateUserContext(StatementContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterImpersonateUser(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitImpersonateUser(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitImpersonateUser(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class RevokeRolesContext extends StatementContext {
		public IdentifierContext catalog;
		public TerminalNode REVOKE() { return getToken(SqlBaseParser.REVOKE, 0); }
		public RolesContext roles() {
			return getRuleContext(RolesContext.class,0);
		}
		public TerminalNode FROM() { return getToken(SqlBaseParser.FROM, 0); }
		public List<PrincipalContext> principal() {
			return getRuleContexts(PrincipalContext.class);
		}
		public PrincipalContext principal(int i) {
			return getRuleContext(PrincipalContext.class,i);
		}
		public TerminalNode ADMIN() { return getToken(SqlBaseParser.ADMIN, 0); }
		public TerminalNode OPTION() { return getToken(SqlBaseParser.OPTION, 0); }
		public TerminalNode FOR() { return getToken(SqlBaseParser.FOR, 0); }
		public TerminalNode GRANTED() { return getToken(SqlBaseParser.GRANTED, 0); }
		public TerminalNode BY() { return getToken(SqlBaseParser.BY, 0); }
		public GrantorContext grantor() {
			return getRuleContext(GrantorContext.class,0);
		}
		public TerminalNode IN() { return getToken(SqlBaseParser.IN, 0); }
		public IdentifierContext identifier() {
			return getRuleContext(IdentifierContext.class,0);
		}
		public RevokeRolesContext(StatementContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterRevokeRoles(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitRevokeRoles(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitRevokeRoles(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class ShowCreateTableContext extends StatementContext {
		public TerminalNode SHOW() { return getToken(SqlBaseParser.SHOW, 0); }
		public TerminalNode CREATE() { return getToken(SqlBaseParser.CREATE, 0); }
		public TerminalNode TABLE() { return getToken(SqlBaseParser.TABLE, 0); }
		public QualifiedNameContext qualifiedName() {
			return getRuleContext(QualifiedNameContext.class,0);
		}
		public ShowCreateTableContext(StatementContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterShowCreateTable(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitShowCreateTable(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitShowCreateTable(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class ShowColumnsContext extends StatementContext {
		public StringContext pattern;
		public StringContext escape;
		public TerminalNode SHOW() { return getToken(SqlBaseParser.SHOW, 0); }
		public TerminalNode COLUMNS() { return getToken(SqlBaseParser.COLUMNS, 0); }
		public TerminalNode FROM() { return getToken(SqlBaseParser.FROM, 0); }
		public TerminalNode IN() { return getToken(SqlBaseParser.IN, 0); }
		public QualifiedNameContext qualifiedName() {
			return getRuleContext(QualifiedNameContext.class,0);
		}
		public TerminalNode LIKE() { return getToken(SqlBaseParser.LIKE, 0); }
		public List<StringContext> string() {
			return getRuleContexts(StringContext.class);
		}
		public StringContext string(int i) {
			return getRuleContext(StringContext.class,i);
		}
		public TerminalNode ESCAPE() { return getToken(SqlBaseParser.ESCAPE, 0); }
		public TerminalNode DESCRIBE() { return getToken(SqlBaseParser.DESCRIBE, 0); }
		public TerminalNode DESC() { return getToken(SqlBaseParser.DESC, 0); }
		public ShowColumnsContext(StatementContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterShowColumns(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitShowColumns(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitShowColumns(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class ShowRoleGrantsContext extends StatementContext {
		public TerminalNode SHOW() { return getToken(SqlBaseParser.SHOW, 0); }
		public TerminalNode ROLE() { return getToken(SqlBaseParser.ROLE, 0); }
		public TerminalNode GRANTS() { return getToken(SqlBaseParser.GRANTS, 0); }
		public IdentifierContext identifier() {
			return getRuleContext(IdentifierContext.class,0);
		}
		public TerminalNode FROM() { return getToken(SqlBaseParser.FROM, 0); }
		public TerminalNode IN() { return getToken(SqlBaseParser.IN, 0); }
		public ShowRoleGrantsContext(StatementContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterShowRoleGrants(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitShowRoleGrants(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitShowRoleGrants(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class AddColumnContext extends StatementContext {
		public QualifiedNameContext tableName;
		public ColumnDefinitionContext column;
		public TerminalNode ALTER() { return getToken(SqlBaseParser.ALTER, 0); }
		public TerminalNode TABLE() { return getToken(SqlBaseParser.TABLE, 0); }
		public TerminalNode ADD() { return getToken(SqlBaseParser.ADD, 0); }
		public TerminalNode COLUMN() { return getToken(SqlBaseParser.COLUMN, 0); }
		public QualifiedNameContext qualifiedName() {
			return getRuleContext(QualifiedNameContext.class,0);
		}
		public ColumnDefinitionContext columnDefinition() {
			return getRuleContext(ColumnDefinitionContext.class,0);
		}
		public List<TerminalNode> IF() { return getTokens(SqlBaseParser.IF); }
		public TerminalNode IF(int i) {
			return getToken(SqlBaseParser.IF, i);
		}
		public List<TerminalNode> EXISTS() { return getTokens(SqlBaseParser.EXISTS); }
		public TerminalNode EXISTS(int i) {
			return getToken(SqlBaseParser.EXISTS, i);
		}
		public TerminalNode NOT() { return getToken(SqlBaseParser.NOT, 0); }
		public AddColumnContext(StatementContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterAddColumn(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitAddColumn(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitAddColumn(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class DenyContext extends StatementContext {
		public PrincipalContext grantee;
		public TerminalNode DENY() { return getToken(SqlBaseParser.DENY, 0); }
		public TerminalNode ON() { return getToken(SqlBaseParser.ON, 0); }
		public QualifiedNameContext qualifiedName() {
			return getRuleContext(QualifiedNameContext.class,0);
		}
		public TerminalNode TO() { return getToken(SqlBaseParser.TO, 0); }
		public PrincipalContext principal() {
			return getRuleContext(PrincipalContext.class,0);
		}
		public List<PrivilegeContext> privilege() {
			return getRuleContexts(PrivilegeContext.class);
		}
		public PrivilegeContext privilege(int i) {
			return getRuleContext(PrivilegeContext.class,i);
		}
		public TerminalNode ALL() { return getToken(SqlBaseParser.ALL, 0); }
		public TerminalNode PRIVILEGES() { return getToken(SqlBaseParser.PRIVILEGES, 0); }
		public TerminalNode SCHEMA() { return getToken(SqlBaseParser.SCHEMA, 0); }
		public TerminalNode TABLE() { return getToken(SqlBaseParser.TABLE, 0); }
		public DenyContext(StatementContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterDeny(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitDeny(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitDeny(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class ResetSessionContext extends StatementContext {
		public TerminalNode RESET() { return getToken(SqlBaseParser.RESET, 0); }
		public TerminalNode SESSION() { return getToken(SqlBaseParser.SESSION, 0); }
		public QualifiedNameContext qualifiedName() {
			return getRuleContext(QualifiedNameContext.class,0);
		}
		public ResetSessionContext(StatementContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterResetSession(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitResetSession(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitResetSession(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class InsertIntoContext extends StatementContext {
		public TerminalNode INSERT() { return getToken(SqlBaseParser.INSERT, 0); }
		public TerminalNode INTO() { return getToken(SqlBaseParser.INTO, 0); }
		public QualifiedNameContext qualifiedName() {
			return getRuleContext(QualifiedNameContext.class,0);
		}
		public QueryContext query() {
			return getRuleContext(QueryContext.class,0);
		}
		public ColumnAliasesContext columnAliases() {
			return getRuleContext(ColumnAliasesContext.class,0);
		}
		public InsertIntoContext(StatementContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterInsertInto(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitInsertInto(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitInsertInto(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class ShowSessionContext extends StatementContext {
		public StringContext pattern;
		public StringContext escape;
		public TerminalNode SHOW() { return getToken(SqlBaseParser.SHOW, 0); }
		public TerminalNode SESSION() { return getToken(SqlBaseParser.SESSION, 0); }
		public TerminalNode LIKE() { return getToken(SqlBaseParser.LIKE, 0); }
		public List<StringContext> string() {
			return getRuleContexts(StringContext.class);
		}
		public StringContext string(int i) {
			return getRuleContext(StringContext.class,i);
		}
		public TerminalNode ESCAPE() { return getToken(SqlBaseParser.ESCAPE, 0); }
		public ShowSessionContext(StatementContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterShowSession(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitShowSession(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitShowSession(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class CreateSchemaContext extends StatementContext {
		public TerminalNode CREATE() { return getToken(SqlBaseParser.CREATE, 0); }
		public TerminalNode SCHEMA() { return getToken(SqlBaseParser.SCHEMA, 0); }
		public QualifiedNameContext qualifiedName() {
			return getRuleContext(QualifiedNameContext.class,0);
		}
		public TerminalNode IF() { return getToken(SqlBaseParser.IF, 0); }
		public TerminalNode NOT() { return getToken(SqlBaseParser.NOT, 0); }
		public TerminalNode EXISTS() { return getToken(SqlBaseParser.EXISTS, 0); }
		public TerminalNode AUTHORIZATION() { return getToken(SqlBaseParser.AUTHORIZATION, 0); }
		public PrincipalContext principal() {
			return getRuleContext(PrincipalContext.class,0);
		}
		public TerminalNode WITH() { return getToken(SqlBaseParser.WITH, 0); }
		public PropertiesContext properties() {
			return getRuleContext(PropertiesContext.class,0);
		}
		public CreateSchemaContext(StatementContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterCreateSchema(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitCreateSchema(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitCreateSchema(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class ExplainAnalyzeContext extends StatementContext {
		public TerminalNode EXPLAIN() { return getToken(SqlBaseParser.EXPLAIN, 0); }
		public TerminalNode ANALYZE() { return getToken(SqlBaseParser.ANALYZE, 0); }
		public StatementContext statement() {
			return getRuleContext(StatementContext.class,0);
		}
		public TerminalNode VERBOSE() { return getToken(SqlBaseParser.VERBOSE, 0); }
		public ExplainAnalyzeContext(StatementContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterExplainAnalyze(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitExplainAnalyze(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitExplainAnalyze(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class ExecuteContext extends StatementContext {
		public TerminalNode EXECUTE() { return getToken(SqlBaseParser.EXECUTE, 0); }
		public IdentifierContext identifier() {
			return getRuleContext(IdentifierContext.class,0);
		}
		public TerminalNode USING() { return getToken(SqlBaseParser.USING, 0); }
		public List<ExpressionContext> expression() {
			return getRuleContexts(ExpressionContext.class);
		}
		public ExpressionContext expression(int i) {
			return getRuleContext(ExpressionContext.class,i);
		}
		public ExecuteContext(StatementContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterExecute(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitExecute(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitExecute(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class RenameSchemaContext extends StatementContext {
		public TerminalNode ALTER() { return getToken(SqlBaseParser.ALTER, 0); }
		public TerminalNode SCHEMA() { return getToken(SqlBaseParser.SCHEMA, 0); }
		public QualifiedNameContext qualifiedName() {
			return getRuleContext(QualifiedNameContext.class,0);
		}
		public TerminalNode RENAME() { return getToken(SqlBaseParser.RENAME, 0); }
		public TerminalNode TO() { return getToken(SqlBaseParser.TO, 0); }
		public IdentifierContext identifier() {
			return getRuleContext(IdentifierContext.class,0);
		}
		public RenameSchemaContext(StatementContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterRenameSchema(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitRenameSchema(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitRenameSchema(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class DropRoleContext extends StatementContext {
		public IdentifierContext name;
		public IdentifierContext catalog;
		public TerminalNode DROP() { return getToken(SqlBaseParser.DROP, 0); }
		public TerminalNode ROLE() { return getToken(SqlBaseParser.ROLE, 0); }
		public List<IdentifierContext> identifier() {
			return getRuleContexts(IdentifierContext.class);
		}
		public IdentifierContext identifier(int i) {
			return getRuleContext(IdentifierContext.class,i);
		}
		public TerminalNode IN() { return getToken(SqlBaseParser.IN, 0); }
		public DropRoleContext(StatementContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterDropRole(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitDropRole(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitDropRole(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class AnalyzeContext extends StatementContext {
		public TerminalNode ANALYZE() { return getToken(SqlBaseParser.ANALYZE, 0); }
		public QualifiedNameContext qualifiedName() {
			return getRuleContext(QualifiedNameContext.class,0);
		}
		public TerminalNode WITH() { return getToken(SqlBaseParser.WITH, 0); }
		public PropertiesContext properties() {
			return getRuleContext(PropertiesContext.class,0);
		}
		public AnalyzeContext(StatementContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterAnalyze(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitAnalyze(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitAnalyze(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class SetRoleContext extends StatementContext {
		public IdentifierContext role;
		public IdentifierContext catalog;
		public TerminalNode SET() { return getToken(SqlBaseParser.SET, 0); }
		public TerminalNode ROLE() { return getToken(SqlBaseParser.ROLE, 0); }
		public TerminalNode ALL() { return getToken(SqlBaseParser.ALL, 0); }
		public TerminalNode NONE() { return getToken(SqlBaseParser.NONE, 0); }
		public List<IdentifierContext> identifier() {
			return getRuleContexts(IdentifierContext.class);
		}
		public IdentifierContext identifier(int i) {
			return getRuleContext(IdentifierContext.class,i);
		}
		public TerminalNode IN() { return getToken(SqlBaseParser.IN, 0); }
		public SetRoleContext(StatementContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterSetRole(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitSetRole(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitSetRole(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class ShowGrantsContext extends StatementContext {
		public TerminalNode SHOW() { return getToken(SqlBaseParser.SHOW, 0); }
		public TerminalNode GRANTS() { return getToken(SqlBaseParser.GRANTS, 0); }
		public TerminalNode ON() { return getToken(SqlBaseParser.ON, 0); }
		public QualifiedNameContext qualifiedName() {
			return getRuleContext(QualifiedNameContext.class,0);
		}
		public TerminalNode TABLE() { return getToken(SqlBaseParser.TABLE, 0); }
		public ShowGrantsContext(StatementContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterShowGrants(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitShowGrants(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitShowGrants(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class DropSchemaContext extends StatementContext {
		public TerminalNode DROP() { return getToken(SqlBaseParser.DROP, 0); }
		public TerminalNode SCHEMA() { return getToken(SqlBaseParser.SCHEMA, 0); }
		public QualifiedNameContext qualifiedName() {
			return getRuleContext(QualifiedNameContext.class,0);
		}
		public TerminalNode IF() { return getToken(SqlBaseParser.IF, 0); }
		public TerminalNode EXISTS() { return getToken(SqlBaseParser.EXISTS, 0); }
		public TerminalNode CASCADE() { return getToken(SqlBaseParser.CASCADE, 0); }
		public TerminalNode RESTRICT() { return getToken(SqlBaseParser.RESTRICT, 0); }
		public DropSchemaContext(StatementContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterDropSchema(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitDropSchema(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitDropSchema(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class SetTableAuthorizationContext extends StatementContext {
		public QualifiedNameContext tableName;
		public TerminalNode ALTER() { return getToken(SqlBaseParser.ALTER, 0); }
		public TerminalNode TABLE() { return getToken(SqlBaseParser.TABLE, 0); }
		public TerminalNode SET() { return getToken(SqlBaseParser.SET, 0); }
		public TerminalNode AUTHORIZATION() { return getToken(SqlBaseParser.AUTHORIZATION, 0); }
		public PrincipalContext principal() {
			return getRuleContext(PrincipalContext.class,0);
		}
		public QualifiedNameContext qualifiedName() {
			return getRuleContext(QualifiedNameContext.class,0);
		}
		public SetTableAuthorizationContext(StatementContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterSetTableAuthorization(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitSetTableAuthorization(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitSetTableAuthorization(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class ShowCreateViewContext extends StatementContext {
		public TerminalNode SHOW() { return getToken(SqlBaseParser.SHOW, 0); }
		public TerminalNode CREATE() { return getToken(SqlBaseParser.CREATE, 0); }
		public TerminalNode VIEW() { return getToken(SqlBaseParser.VIEW, 0); }
		public QualifiedNameContext qualifiedName() {
			return getRuleContext(QualifiedNameContext.class,0);
		}
		public ShowCreateViewContext(StatementContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterShowCreateView(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitShowCreateView(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitShowCreateView(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class CreateTableContext extends StatementContext {
		public TerminalNode CREATE() { return getToken(SqlBaseParser.CREATE, 0); }
		public TerminalNode TABLE() { return getToken(SqlBaseParser.TABLE, 0); }
		public QualifiedNameContext qualifiedName() {
			return getRuleContext(QualifiedNameContext.class,0);
		}
		public List<TableElementContext> tableElement() {
			return getRuleContexts(TableElementContext.class);
		}
		public TableElementContext tableElement(int i) {
			return getRuleContext(TableElementContext.class,i);
		}
		public TerminalNode IF() { return getToken(SqlBaseParser.IF, 0); }
		public TerminalNode NOT() { return getToken(SqlBaseParser.NOT, 0); }
		public TerminalNode EXISTS() { return getToken(SqlBaseParser.EXISTS, 0); }
		public TerminalNode COMMENT() { return getToken(SqlBaseParser.COMMENT, 0); }
		public StringContext string() {
			return getRuleContext(StringContext.class,0);
		}
		public TerminalNode WITH() { return getToken(SqlBaseParser.WITH, 0); }
		public PropertiesContext properties() {
			return getRuleContext(PropertiesContext.class,0);
		}
		public CreateTableContext(StatementContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterCreateTable(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitCreateTable(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitCreateTable(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class StartTransactionContext extends StatementContext {
		public TerminalNode START() { return getToken(SqlBaseParser.START, 0); }
		public TerminalNode TRANSACTION() { return getToken(SqlBaseParser.TRANSACTION, 0); }
		public List<TransactionModeContext> transactionMode() {
			return getRuleContexts(TransactionModeContext.class);
		}
		public TransactionModeContext transactionMode(int i) {
			return getRuleContext(TransactionModeContext.class,i);
		}
		public StartTransactionContext(StatementContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterStartTransaction(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitStartTransaction(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitStartTransaction(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class CreateTableAsSelectContext extends StatementContext {
		public TerminalNode CREATE() { return getToken(SqlBaseParser.CREATE, 0); }
		public TerminalNode TABLE() { return getToken(SqlBaseParser.TABLE, 0); }
		public QualifiedNameContext qualifiedName() {
			return getRuleContext(QualifiedNameContext.class,0);
		}
		public TerminalNode AS() { return getToken(SqlBaseParser.AS, 0); }
		public QueryContext query() {
			return getRuleContext(QueryContext.class,0);
		}
		public TerminalNode IF() { return getToken(SqlBaseParser.IF, 0); }
		public TerminalNode NOT() { return getToken(SqlBaseParser.NOT, 0); }
		public TerminalNode EXISTS() { return getToken(SqlBaseParser.EXISTS, 0); }
		public ColumnAliasesContext columnAliases() {
			return getRuleContext(ColumnAliasesContext.class,0);
		}
		public TerminalNode COMMENT() { return getToken(SqlBaseParser.COMMENT, 0); }
		public StringContext string() {
			return getRuleContext(StringContext.class,0);
		}
		public List<TerminalNode> WITH() { return getTokens(SqlBaseParser.WITH); }
		public TerminalNode WITH(int i) {
			return getToken(SqlBaseParser.WITH, i);
		}
		public PropertiesContext properties() {
			return getRuleContext(PropertiesContext.class,0);
		}
		public TerminalNode DATA() { return getToken(SqlBaseParser.DATA, 0); }
		public TerminalNode NO() { return getToken(SqlBaseParser.NO, 0); }
		public CreateTableAsSelectContext(StatementContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterCreateTableAsSelect(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitCreateTableAsSelect(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitCreateTableAsSelect(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class ShowStatsContext extends StatementContext {
		public TerminalNode SHOW() { return getToken(SqlBaseParser.SHOW, 0); }
		public TerminalNode STATS() { return getToken(SqlBaseParser.STATS, 0); }
		public TerminalNode FOR() { return getToken(SqlBaseParser.FOR, 0); }
		public QualifiedNameContext qualifiedName() {
			return getRuleContext(QualifiedNameContext.class,0);
		}
		public ShowStatsContext(StatementContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterShowStats(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitShowStats(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitShowStats(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class ShowCreateSchemaContext extends StatementContext {
		public TerminalNode SHOW() { return getToken(SqlBaseParser.SHOW, 0); }
		public TerminalNode CREATE() { return getToken(SqlBaseParser.CREATE, 0); }
		public TerminalNode SCHEMA() { return getToken(SqlBaseParser.SCHEMA, 0); }
		public QualifiedNameContext qualifiedName() {
			return getRuleContext(QualifiedNameContext.class,0);
		}
		public ShowCreateSchemaContext(StatementContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterShowCreateSchema(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitShowCreateSchema(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitShowCreateSchema(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class RevokeContext extends StatementContext {
		public PrincipalContext grantee;
		public TerminalNode REVOKE() { return getToken(SqlBaseParser.REVOKE, 0); }
		public TerminalNode ON() { return getToken(SqlBaseParser.ON, 0); }
		public QualifiedNameContext qualifiedName() {
			return getRuleContext(QualifiedNameContext.class,0);
		}
		public TerminalNode FROM() { return getToken(SqlBaseParser.FROM, 0); }
		public PrincipalContext principal() {
			return getRuleContext(PrincipalContext.class,0);
		}
		public List<PrivilegeContext> privilege() {
			return getRuleContexts(PrivilegeContext.class);
		}
		public PrivilegeContext privilege(int i) {
			return getRuleContext(PrivilegeContext.class,i);
		}
		public TerminalNode ALL() { return getToken(SqlBaseParser.ALL, 0); }
		public TerminalNode PRIVILEGES() { return getToken(SqlBaseParser.PRIVILEGES, 0); }
		public TerminalNode GRANT() { return getToken(SqlBaseParser.GRANT, 0); }
		public TerminalNode OPTION() { return getToken(SqlBaseParser.OPTION, 0); }
		public TerminalNode FOR() { return getToken(SqlBaseParser.FOR, 0); }
		public TerminalNode SCHEMA() { return getToken(SqlBaseParser.SCHEMA, 0); }
		public TerminalNode TABLE() { return getToken(SqlBaseParser.TABLE, 0); }
		public RevokeContext(StatementContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterRevoke(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitRevoke(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitRevoke(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class UpdateContext extends StatementContext {
		public BooleanExpressionContext where;
		public TerminalNode UPDATE() { return getToken(SqlBaseParser.UPDATE, 0); }
		public QualifiedNameContext qualifiedName() {
			return getRuleContext(QualifiedNameContext.class,0);
		}
		public TerminalNode SET() { return getToken(SqlBaseParser.SET, 0); }
		public List<UpdateAssignmentContext> updateAssignment() {
			return getRuleContexts(UpdateAssignmentContext.class);
		}
		public UpdateAssignmentContext updateAssignment(int i) {
			return getRuleContext(UpdateAssignmentContext.class,i);
		}
		public TerminalNode WHERE() { return getToken(SqlBaseParser.WHERE, 0); }
		public BooleanExpressionContext booleanExpression() {
			return getRuleContext(BooleanExpressionContext.class,0);
		}
		public UpdateContext(StatementContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterUpdate(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitUpdate(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitUpdate(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class TableExecuteContext extends StatementContext {
		public QualifiedNameContext tableName;
		public IdentifierContext procedureName;
		public BooleanExpressionContext where;
		public TerminalNode ALTER() { return getToken(SqlBaseParser.ALTER, 0); }
		public TerminalNode TABLE() { return getToken(SqlBaseParser.TABLE, 0); }
		public TerminalNode EXECUTE() { return getToken(SqlBaseParser.EXECUTE, 0); }
		public QualifiedNameContext qualifiedName() {
			return getRuleContext(QualifiedNameContext.class,0);
		}
		public IdentifierContext identifier() {
			return getRuleContext(IdentifierContext.class,0);
		}
		public TerminalNode WHERE() { return getToken(SqlBaseParser.WHERE, 0); }
		public BooleanExpressionContext booleanExpression() {
			return getRuleContext(BooleanExpressionContext.class,0);
		}
		public List<CallArgumentContext> callArgument() {
			return getRuleContexts(CallArgumentContext.class);
		}
		public CallArgumentContext callArgument(int i) {
			return getRuleContext(CallArgumentContext.class,i);
		}
		public TableExecuteContext(StatementContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterTableExecute(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitTableExecute(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitTableExecute(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class DeleteContext extends StatementContext {
		public TerminalNode DELETE() { return getToken(SqlBaseParser.DELETE, 0); }
		public TerminalNode FROM() { return getToken(SqlBaseParser.FROM, 0); }
		public QualifiedNameContext qualifiedName() {
			return getRuleContext(QualifiedNameContext.class,0);
		}
		public TerminalNode WHERE() { return getToken(SqlBaseParser.WHERE, 0); }
		public BooleanExpressionContext booleanExpression() {
			return getRuleContext(BooleanExpressionContext.class,0);
		}
		public DeleteContext(StatementContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterDelete(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitDelete(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitDelete(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class DescribeInputContext extends StatementContext {
		public TerminalNode DESCRIBE() { return getToken(SqlBaseParser.DESCRIBE, 0); }
		public TerminalNode INPUT() { return getToken(SqlBaseParser.INPUT, 0); }
		public IdentifierContext identifier() {
			return getRuleContext(IdentifierContext.class,0);
		}
		public DescribeInputContext(StatementContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterDescribeInput(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitDescribeInput(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitDescribeInput(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class ShowStatsForQueryContext extends StatementContext {
		public TerminalNode SHOW() { return getToken(SqlBaseParser.SHOW, 0); }
		public TerminalNode STATS() { return getToken(SqlBaseParser.STATS, 0); }
		public TerminalNode FOR() { return getToken(SqlBaseParser.FOR, 0); }
		public QueryContext query() {
			return getRuleContext(QueryContext.class,0);
		}
		public ShowStatsForQueryContext(StatementContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterShowStatsForQuery(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitShowStatsForQuery(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitShowStatsForQuery(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class StatementDefaultContext extends StatementContext {
		public QueryContext query() {
			return getRuleContext(QueryContext.class,0);
		}
		public StatementDefaultContext(StatementContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterStatementDefault(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitStatementDefault(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitStatementDefault(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class DeclareCursorContext extends StatementContext {
		public IdentifierContext name;
		public QueryContext body;
		public TerminalNode DECLARE() { return getToken(SqlBaseParser.DECLARE, 0); }
		public TerminalNode CURSOR() { return getToken(SqlBaseParser.CURSOR, 0); }
		public TerminalNode FOR() { return getToken(SqlBaseParser.FOR, 0); }
		public IdentifierContext identifier() {
			return getRuleContext(IdentifierContext.class,0);
		}
		public QueryContext query() {
			return getRuleContext(QueryContext.class,0);
		}
		public TerminalNode WITH() { return getToken(SqlBaseParser.WITH, 0); }
		public TerminalNode WITHOUT() { return getToken(SqlBaseParser.WITHOUT, 0); }
		public TerminalNode NO() { return getToken(SqlBaseParser.NO, 0); }
		public DeclareCursorContext(StatementContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterDeclareCursor(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitDeclareCursor(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitDeclareCursor(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class SetTimeZoneContext extends StatementContext {
		public TerminalNode SET() { return getToken(SqlBaseParser.SET, 0); }
		public TerminalNode TIME() { return getToken(SqlBaseParser.TIME, 0); }
		public TerminalNode ZONE() { return getToken(SqlBaseParser.ZONE, 0); }
		public TerminalNode LOCAL() { return getToken(SqlBaseParser.LOCAL, 0); }
		public ExpressionContext expression() {
			return getRuleContext(ExpressionContext.class,0);
		}
		public SetTimeZoneContext(StatementContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterSetTimeZone(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitSetTimeZone(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitSetTimeZone(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class TruncateTableContext extends StatementContext {
		public TerminalNode TRUNCATE() { return getToken(SqlBaseParser.TRUNCATE, 0); }
		public TerminalNode TABLE() { return getToken(SqlBaseParser.TABLE, 0); }
		public QualifiedNameContext qualifiedName() {
			return getRuleContext(QualifiedNameContext.class,0);
		}
		public TruncateTableContext(StatementContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterTruncateTable(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitTruncateTable(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitTruncateTable(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class CreateMaterializedViewContext extends StatementContext {
		public TerminalNode CREATE() { return getToken(SqlBaseParser.CREATE, 0); }
		public TerminalNode MATERIALIZED() { return getToken(SqlBaseParser.MATERIALIZED, 0); }
		public TerminalNode VIEW() { return getToken(SqlBaseParser.VIEW, 0); }
		public QualifiedNameContext qualifiedName() {
			return getRuleContext(QualifiedNameContext.class,0);
		}
		public TerminalNode AS() { return getToken(SqlBaseParser.AS, 0); }
		public QueryContext query() {
			return getRuleContext(QueryContext.class,0);
		}
		public TerminalNode OR() { return getToken(SqlBaseParser.OR, 0); }
		public TerminalNode REPLACE() { return getToken(SqlBaseParser.REPLACE, 0); }
		public TerminalNode IF() { return getToken(SqlBaseParser.IF, 0); }
		public TerminalNode NOT() { return getToken(SqlBaseParser.NOT, 0); }
		public TerminalNode EXISTS() { return getToken(SqlBaseParser.EXISTS, 0); }
		public TerminalNode COMMENT() { return getToken(SqlBaseParser.COMMENT, 0); }
		public StringContext string() {
			return getRuleContext(StringContext.class,0);
		}
		public TerminalNode WITH() { return getToken(SqlBaseParser.WITH, 0); }
		public PropertiesContext properties() {
			return getRuleContext(PropertiesContext.class,0);
		}
		public CreateMaterializedViewContext(StatementContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterCreateMaterializedView(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitCreateMaterializedView(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitCreateMaterializedView(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class SetSessionContext extends StatementContext {
		public TerminalNode SET() { return getToken(SqlBaseParser.SET, 0); }
		public TerminalNode SESSION() { return getToken(SqlBaseParser.SESSION, 0); }
		public QualifiedNameContext qualifiedName() {
			return getRuleContext(QualifiedNameContext.class,0);
		}
		public TerminalNode EQ() { return getToken(SqlBaseParser.EQ, 0); }
		public ExpressionContext expression() {
			return getRuleContext(ExpressionContext.class,0);
		}
		public SetSessionContext(StatementContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterSetSession(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitSetSession(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitSetSession(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class CreateViewContext extends StatementContext {
		public TerminalNode CREATE() { return getToken(SqlBaseParser.CREATE, 0); }
		public TerminalNode VIEW() { return getToken(SqlBaseParser.VIEW, 0); }
		public QualifiedNameContext qualifiedName() {
			return getRuleContext(QualifiedNameContext.class,0);
		}
		public TerminalNode AS() { return getToken(SqlBaseParser.AS, 0); }
		public QueryContext query() {
			return getRuleContext(QueryContext.class,0);
		}
		public TerminalNode OR() { return getToken(SqlBaseParser.OR, 0); }
		public TerminalNode REPLACE() { return getToken(SqlBaseParser.REPLACE, 0); }
		public TerminalNode COMMENT() { return getToken(SqlBaseParser.COMMENT, 0); }
		public StringContext string() {
			return getRuleContext(StringContext.class,0);
		}
		public TerminalNode SECURITY() { return getToken(SqlBaseParser.SECURITY, 0); }
		public TerminalNode DEFINER() { return getToken(SqlBaseParser.DEFINER, 0); }
		public TerminalNode INVOKER() { return getToken(SqlBaseParser.INVOKER, 0); }
		public CreateViewContext(StatementContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterCreateView(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitCreateView(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitCreateView(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class RenameMaterializedViewContext extends StatementContext {
		public QualifiedNameContext from;
		public QualifiedNameContext to;
		public TerminalNode ALTER() { return getToken(SqlBaseParser.ALTER, 0); }
		public TerminalNode MATERIALIZED() { return getToken(SqlBaseParser.MATERIALIZED, 0); }
		public TerminalNode VIEW() { return getToken(SqlBaseParser.VIEW, 0); }
		public TerminalNode RENAME() { return getToken(SqlBaseParser.RENAME, 0); }
		public TerminalNode TO() { return getToken(SqlBaseParser.TO, 0); }
		public List<QualifiedNameContext> qualifiedName() {
			return getRuleContexts(QualifiedNameContext.class);
		}
		public QualifiedNameContext qualifiedName(int i) {
			return getRuleContext(QualifiedNameContext.class,i);
		}
		public TerminalNode IF() { return getToken(SqlBaseParser.IF, 0); }
		public TerminalNode EXISTS() { return getToken(SqlBaseParser.EXISTS, 0); }
		public RenameMaterializedViewContext(StatementContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterRenameMaterializedView(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitRenameMaterializedView(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitRenameMaterializedView(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class ShowSchemasContext extends StatementContext {
		public StringContext pattern;
		public StringContext escape;
		public TerminalNode SHOW() { return getToken(SqlBaseParser.SHOW, 0); }
		public TerminalNode SCHEMAS() { return getToken(SqlBaseParser.SCHEMAS, 0); }
		public IdentifierContext identifier() {
			return getRuleContext(IdentifierContext.class,0);
		}
		public TerminalNode LIKE() { return getToken(SqlBaseParser.LIKE, 0); }
		public TerminalNode FROM() { return getToken(SqlBaseParser.FROM, 0); }
		public TerminalNode IN() { return getToken(SqlBaseParser.IN, 0); }
		public List<StringContext> string() {
			return getRuleContexts(StringContext.class);
		}
		public StringContext string(int i) {
			return getRuleContext(StringContext.class,i);
		}
		public TerminalNode ESCAPE() { return getToken(SqlBaseParser.ESCAPE, 0); }
		public ShowSchemasContext(StatementContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterShowSchemas(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitShowSchemas(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitShowSchemas(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class DropTableContext extends StatementContext {
		public TerminalNode DROP() { return getToken(SqlBaseParser.DROP, 0); }
		public TerminalNode TABLE() { return getToken(SqlBaseParser.TABLE, 0); }
		public QualifiedNameContext qualifiedName() {
			return getRuleContext(QualifiedNameContext.class,0);
		}
		public TerminalNode IF() { return getToken(SqlBaseParser.IF, 0); }
		public TerminalNode EXISTS() { return getToken(SqlBaseParser.EXISTS, 0); }
		public DropTableContext(StatementContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterDropTable(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitDropTable(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitDropTable(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class SetSchemaAuthorizationContext extends StatementContext {
		public TerminalNode ALTER() { return getToken(SqlBaseParser.ALTER, 0); }
		public TerminalNode SCHEMA() { return getToken(SqlBaseParser.SCHEMA, 0); }
		public QualifiedNameContext qualifiedName() {
			return getRuleContext(QualifiedNameContext.class,0);
		}
		public TerminalNode SET() { return getToken(SqlBaseParser.SET, 0); }
		public TerminalNode AUTHORIZATION() { return getToken(SqlBaseParser.AUTHORIZATION, 0); }
		public PrincipalContext principal() {
			return getRuleContext(PrincipalContext.class,0);
		}
		public SetSchemaAuthorizationContext(StatementContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterSetSchemaAuthorization(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitSetSchemaAuthorization(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitSetSchemaAuthorization(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class RollbackContext extends StatementContext {
		public TerminalNode ROLLBACK() { return getToken(SqlBaseParser.ROLLBACK, 0); }
		public TerminalNode WORK() { return getToken(SqlBaseParser.WORK, 0); }
		public RollbackContext(StatementContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterRollback(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitRollback(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitRollback(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class CommentTableContext extends StatementContext {
		public TerminalNode COMMENT() { return getToken(SqlBaseParser.COMMENT, 0); }
		public TerminalNode ON() { return getToken(SqlBaseParser.ON, 0); }
		public TerminalNode TABLE() { return getToken(SqlBaseParser.TABLE, 0); }
		public QualifiedNameContext qualifiedName() {
			return getRuleContext(QualifiedNameContext.class,0);
		}
		public TerminalNode IS() { return getToken(SqlBaseParser.IS, 0); }
		public StringContext string() {
			return getRuleContext(StringContext.class,0);
		}
		public TerminalNode NULL() { return getToken(SqlBaseParser.NULL, 0); }
		public CommentTableContext(StatementContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterCommentTable(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitCommentTable(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitCommentTable(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class RenameViewContext extends StatementContext {
		public QualifiedNameContext from;
		public QualifiedNameContext to;
		public TerminalNode ALTER() { return getToken(SqlBaseParser.ALTER, 0); }
		public TerminalNode VIEW() { return getToken(SqlBaseParser.VIEW, 0); }
		public TerminalNode RENAME() { return getToken(SqlBaseParser.RENAME, 0); }
		public TerminalNode TO() { return getToken(SqlBaseParser.TO, 0); }
		public List<QualifiedNameContext> qualifiedName() {
			return getRuleContexts(QualifiedNameContext.class);
		}
		public QualifiedNameContext qualifiedName(int i) {
			return getRuleContext(QualifiedNameContext.class,i);
		}
		public RenameViewContext(StatementContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterRenameView(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitRenameView(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitRenameView(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class SetPathContext extends StatementContext {
		public TerminalNode SET() { return getToken(SqlBaseParser.SET, 0); }
		public TerminalNode PATH() { return getToken(SqlBaseParser.PATH, 0); }
		public PathSpecificationContext pathSpecification() {
			return getRuleContext(PathSpecificationContext.class,0);
		}
		public SetPathContext(StatementContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterSetPath(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitSetPath(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitSetPath(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class GrantRolesContext extends StatementContext {
		public IdentifierContext catalog;
		public TerminalNode GRANT() { return getToken(SqlBaseParser.GRANT, 0); }
		public RolesContext roles() {
			return getRuleContext(RolesContext.class,0);
		}
		public TerminalNode TO() { return getToken(SqlBaseParser.TO, 0); }
		public List<PrincipalContext> principal() {
			return getRuleContexts(PrincipalContext.class);
		}
		public PrincipalContext principal(int i) {
			return getRuleContext(PrincipalContext.class,i);
		}
		public TerminalNode WITH() { return getToken(SqlBaseParser.WITH, 0); }
		public TerminalNode ADMIN() { return getToken(SqlBaseParser.ADMIN, 0); }
		public TerminalNode OPTION() { return getToken(SqlBaseParser.OPTION, 0); }
		public TerminalNode GRANTED() { return getToken(SqlBaseParser.GRANTED, 0); }
		public TerminalNode BY() { return getToken(SqlBaseParser.BY, 0); }
		public GrantorContext grantor() {
			return getRuleContext(GrantorContext.class,0);
		}
		public TerminalNode IN() { return getToken(SqlBaseParser.IN, 0); }
		public IdentifierContext identifier() {
			return getRuleContext(IdentifierContext.class,0);
		}
		public GrantRolesContext(StatementContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterGrantRoles(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitGrantRoles(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitGrantRoles(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class CallContext extends StatementContext {
		public TerminalNode CALL() { return getToken(SqlBaseParser.CALL, 0); }
		public QualifiedNameContext qualifiedName() {
			return getRuleContext(QualifiedNameContext.class,0);
		}
		public List<CallArgumentContext> callArgument() {
			return getRuleContexts(CallArgumentContext.class);
		}
		public CallArgumentContext callArgument(int i) {
			return getRuleContext(CallArgumentContext.class,i);
		}
		public CallContext(StatementContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterCall(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitCall(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitCall(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class RefreshMaterializedViewContext extends StatementContext {
		public TerminalNode REFRESH() { return getToken(SqlBaseParser.REFRESH, 0); }
		public TerminalNode MATERIALIZED() { return getToken(SqlBaseParser.MATERIALIZED, 0); }
		public TerminalNode VIEW() { return getToken(SqlBaseParser.VIEW, 0); }
		public QualifiedNameContext qualifiedName() {
			return getRuleContext(QualifiedNameContext.class,0);
		}
		public RefreshMaterializedViewContext(StatementContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterRefreshMaterializedView(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitRefreshMaterializedView(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitRefreshMaterializedView(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class ShowCreateMaterializedViewContext extends StatementContext {
		public TerminalNode SHOW() { return getToken(SqlBaseParser.SHOW, 0); }
		public TerminalNode CREATE() { return getToken(SqlBaseParser.CREATE, 0); }
		public TerminalNode MATERIALIZED() { return getToken(SqlBaseParser.MATERIALIZED, 0); }
		public TerminalNode VIEW() { return getToken(SqlBaseParser.VIEW, 0); }
		public QualifiedNameContext qualifiedName() {
			return getRuleContext(QualifiedNameContext.class,0);
		}
		public ShowCreateMaterializedViewContext(StatementContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterShowCreateMaterializedView(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitShowCreateMaterializedView(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitShowCreateMaterializedView(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class ShowFunctionsContext extends StatementContext {
		public StringContext pattern;
		public StringContext escape;
		public TerminalNode SHOW() { return getToken(SqlBaseParser.SHOW, 0); }
		public TerminalNode FUNCTIONS() { return getToken(SqlBaseParser.FUNCTIONS, 0); }
		public TerminalNode LIKE() { return getToken(SqlBaseParser.LIKE, 0); }
		public List<StringContext> string() {
			return getRuleContexts(StringContext.class);
		}
		public StringContext string(int i) {
			return getRuleContext(StringContext.class,i);
		}
		public TerminalNode ESCAPE() { return getToken(SqlBaseParser.ESCAPE, 0); }
		public ShowFunctionsContext(StatementContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterShowFunctions(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitShowFunctions(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitShowFunctions(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class DescribeOutputContext extends StatementContext {
		public TerminalNode DESCRIBE() { return getToken(SqlBaseParser.DESCRIBE, 0); }
		public TerminalNode OUTPUT() { return getToken(SqlBaseParser.OUTPUT, 0); }
		public IdentifierContext identifier() {
			return getRuleContext(IdentifierContext.class,0);
		}
		public DescribeOutputContext(StatementContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterDescribeOutput(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitDescribeOutput(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitDescribeOutput(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class GrantContext extends StatementContext {
		public PrincipalContext grantee;
		public List<TerminalNode> GRANT() { return getTokens(SqlBaseParser.GRANT); }
		public TerminalNode GRANT(int i) {
			return getToken(SqlBaseParser.GRANT, i);
		}
		public TerminalNode ON() { return getToken(SqlBaseParser.ON, 0); }
		public QualifiedNameContext qualifiedName() {
			return getRuleContext(QualifiedNameContext.class,0);
		}
		public TerminalNode TO() { return getToken(SqlBaseParser.TO, 0); }
		public PrincipalContext principal() {
			return getRuleContext(PrincipalContext.class,0);
		}
		public List<PrivilegeContext> privilege() {
			return getRuleContexts(PrivilegeContext.class);
		}
		public PrivilegeContext privilege(int i) {
			return getRuleContext(PrivilegeContext.class,i);
		}
		public TerminalNode ALL() { return getToken(SqlBaseParser.ALL, 0); }
		public TerminalNode PRIVILEGES() { return getToken(SqlBaseParser.PRIVILEGES, 0); }
		public TerminalNode WITH() { return getToken(SqlBaseParser.WITH, 0); }
		public TerminalNode OPTION() { return getToken(SqlBaseParser.OPTION, 0); }
		public TerminalNode SCHEMA() { return getToken(SqlBaseParser.SCHEMA, 0); }
		public TerminalNode TABLE() { return getToken(SqlBaseParser.TABLE, 0); }
		public GrantContext(StatementContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterGrant(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitGrant(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitGrant(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class SetTablePropertiesContext extends StatementContext {
		public QualifiedNameContext tableName;
		public TerminalNode ALTER() { return getToken(SqlBaseParser.ALTER, 0); }
		public TerminalNode TABLE() { return getToken(SqlBaseParser.TABLE, 0); }
		public TerminalNode SET() { return getToken(SqlBaseParser.SET, 0); }
		public TerminalNode PROPERTIES() { return getToken(SqlBaseParser.PROPERTIES, 0); }
		public PropertyAssignmentsContext propertyAssignments() {
			return getRuleContext(PropertyAssignmentsContext.class,0);
		}
		public QualifiedNameContext qualifiedName() {
			return getRuleContext(QualifiedNameContext.class,0);
		}
		public SetTablePropertiesContext(StatementContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterSetTableProperties(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitSetTableProperties(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitSetTableProperties(this);
			else return visitor.visitChildren(this);
		}
	}

	public final StatementContext statement() throws RecognitionException {
		StatementContext _localctx = new StatementContext(_ctx, getState());
		enterRule(_localctx, 10, RULE_statement);
		int _la;
		try {
			setState(999);
			_errHandler.sync(this);
			switch ( getInterpreter().adaptivePredict(_input,109,_ctx) ) {
			case 1:
				_localctx = new StatementDefaultContext(_localctx);
				enterOuterAlt(_localctx, 1);
				{
				setState(207);
				query();
				}
				break;
			case 2:
				_localctx = new UseContext(_localctx);
				enterOuterAlt(_localctx, 2);
				{
				setState(208);
				match(USE);
				setState(209);
				((UseContext)_localctx).schema = identifier();
				}
				break;
			case 3:
				_localctx = new UseContext(_localctx);
				enterOuterAlt(_localctx, 3);
				{
				setState(210);
				match(USE);
				setState(211);
				((UseContext)_localctx).catalog = identifier();
				setState(212);
				match(T__0);
				setState(213);
				((UseContext)_localctx).schema = identifier();
				}
				break;
			case 4:
				_localctx = new CreateSchemaContext(_localctx);
				enterOuterAlt(_localctx, 4);
				{
				setState(215);
				match(CREATE);
				setState(216);
				match(SCHEMA);
				setState(220);
				_errHandler.sync(this);
				switch ( getInterpreter().adaptivePredict(_input,0,_ctx) ) {
				case 1:
					{
					setState(217);
					match(IF);
					setState(218);
					match(NOT);
					setState(219);
					match(EXISTS);
					}
					break;
				}
				setState(222);
				qualifiedName();
				setState(225);
				_errHandler.sync(this);
				_la = _input.LA(1);
				if (_la==AUTHORIZATION) {
					{
					setState(223);
					match(AUTHORIZATION);
					setState(224);
					principal();
					}
				}

				setState(229);
				_errHandler.sync(this);
				_la = _input.LA(1);
				if (_la==WITH) {
					{
					setState(227);
					match(WITH);
					setState(228);
					properties();
					}
				}

				}
				break;
			case 5:
				_localctx = new DropSchemaContext(_localctx);
				enterOuterAlt(_localctx, 5);
				{
				setState(231);
				match(DROP);
				setState(232);
				match(SCHEMA);
				setState(235);
				_errHandler.sync(this);
				switch ( getInterpreter().adaptivePredict(_input,3,_ctx) ) {
				case 1:
					{
					setState(233);
					match(IF);
					setState(234);
					match(EXISTS);
					}
					break;
				}
				setState(237);
				qualifiedName();
				setState(239);
				_errHandler.sync(this);
				_la = _input.LA(1);
				if (_la==CASCADE || _la==RESTRICT) {
					{
					setState(238);
					_la = _input.LA(1);
					if ( !(_la==CASCADE || _la==RESTRICT) ) {
					_errHandler.recoverInline(this);
					}
					else {
						if ( _input.LA(1)==Token.EOF ) matchedEOF = true;
						_errHandler.reportMatch(this);
						consume();
					}
					}
				}

				}
				break;
			case 6:
				_localctx = new RenameSchemaContext(_localctx);
				enterOuterAlt(_localctx, 6);
				{
				setState(241);
				match(ALTER);
				setState(242);
				match(SCHEMA);
				setState(243);
				qualifiedName();
				setState(244);
				match(RENAME);
				setState(245);
				match(TO);
				setState(246);
				identifier();
				}
				break;
			case 7:
				_localctx = new SetSchemaAuthorizationContext(_localctx);
				enterOuterAlt(_localctx, 7);
				{
				setState(248);
				match(ALTER);
				setState(249);
				match(SCHEMA);
				setState(250);
				qualifiedName();
				setState(251);
				match(SET);
				setState(252);
				match(AUTHORIZATION);
				setState(253);
				principal();
				}
				break;
			case 8:
				_localctx = new CreateTableAsSelectContext(_localctx);
				enterOuterAlt(_localctx, 8);
				{
				setState(255);
				match(CREATE);
				setState(256);
				match(TABLE);
				setState(260);
				_errHandler.sync(this);
				switch ( getInterpreter().adaptivePredict(_input,5,_ctx) ) {
				case 1:
					{
					setState(257);
					match(IF);
					setState(258);
					match(NOT);
					setState(259);
					match(EXISTS);
					}
					break;
				}
				setState(262);
				qualifiedName();
				setState(264);
				_errHandler.sync(this);
				_la = _input.LA(1);
				if (_la==T__1) {
					{
					setState(263);
					columnAliases();
					}
				}

				setState(268);
				_errHandler.sync(this);
				_la = _input.LA(1);
				if (_la==COMMENT) {
					{
					setState(266);
					match(COMMENT);
					setState(267);
					string();
					}
				}

				setState(272);
				_errHandler.sync(this);
				_la = _input.LA(1);
				if (_la==WITH) {
					{
					setState(270);
					match(WITH);
					setState(271);
					properties();
					}
				}

				setState(274);
				match(AS);
				setState(280);
				_errHandler.sync(this);
				switch ( getInterpreter().adaptivePredict(_input,9,_ctx) ) {
				case 1:
					{
					setState(275);
					query();
					}
					break;
				case 2:
					{
					setState(276);
					match(T__1);
					setState(277);
					query();
					setState(278);
					match(T__2);
					}
					break;
				}
				setState(287);
				_errHandler.sync(this);
				_la = _input.LA(1);
				if (_la==WITH) {
					{
					setState(282);
					match(WITH);
					setState(284);
					_errHandler.sync(this);
					_la = _input.LA(1);
					if (_la==NO) {
						{
						setState(283);
						match(NO);
						}
					}

					setState(286);
					match(DATA);
					}
				}

				}
				break;
			case 9:
				_localctx = new CreateTableContext(_localctx);
				enterOuterAlt(_localctx, 9);
				{
				setState(289);
				match(CREATE);
				setState(290);
				match(TABLE);
				setState(294);
				_errHandler.sync(this);
				switch ( getInterpreter().adaptivePredict(_input,12,_ctx) ) {
				case 1:
					{
					setState(291);
					match(IF);
					setState(292);
					match(NOT);
					setState(293);
					match(EXISTS);
					}
					break;
				}
				setState(296);
				qualifiedName();
				setState(297);
				match(T__1);
				setState(298);
				tableElement();
				setState(303);
				_errHandler.sync(this);
				_la = _input.LA(1);
				while (_la==T__3) {
					{
					{
					setState(299);
					match(T__3);
					setState(300);
					tableElement();
					}
					}
					setState(305);
					_errHandler.sync(this);
					_la = _input.LA(1);
				}
				setState(306);
				match(T__2);
				setState(309);
				_errHandler.sync(this);
				_la = _input.LA(1);
				if (_la==COMMENT) {
					{
					setState(307);
					match(COMMENT);
					setState(308);
					string();
					}
				}

				setState(313);
				_errHandler.sync(this);
				_la = _input.LA(1);
				if (_la==WITH) {
					{
					setState(311);
					match(WITH);
					setState(312);
					properties();
					}
				}

				}
				break;
			case 10:
				_localctx = new DropTableContext(_localctx);
				enterOuterAlt(_localctx, 10);
				{
				setState(315);
				match(DROP);
				setState(316);
				match(TABLE);
				setState(319);
				_errHandler.sync(this);
				switch ( getInterpreter().adaptivePredict(_input,16,_ctx) ) {
				case 1:
					{
					setState(317);
					match(IF);
					setState(318);
					match(EXISTS);
					}
					break;
				}
				setState(321);
				qualifiedName();
				}
				break;
			case 11:
				_localctx = new InsertIntoContext(_localctx);
				enterOuterAlt(_localctx, 11);
				{
				setState(322);
				match(INSERT);
				setState(323);
				match(INTO);
				setState(324);
				qualifiedName();
				setState(326);
				_errHandler.sync(this);
				switch ( getInterpreter().adaptivePredict(_input,17,_ctx) ) {
				case 1:
					{
					setState(325);
					columnAliases();
					}
					break;
				}
				setState(328);
				query();
				}
				break;
			case 12:
				_localctx = new DeleteContext(_localctx);
				enterOuterAlt(_localctx, 12);
				{
				setState(330);
				match(DELETE);
				setState(331);
				match(FROM);
				setState(332);
				qualifiedName();
				setState(335);
				_errHandler.sync(this);
				_la = _input.LA(1);
				if (_la==WHERE) {
					{
					setState(333);
					match(WHERE);
					setState(334);
					booleanExpression(0);
					}
				}

				}
				break;
			case 13:
				_localctx = new TruncateTableContext(_localctx);
				enterOuterAlt(_localctx, 13);
				{
				setState(337);
				match(TRUNCATE);
				setState(338);
				match(TABLE);
				setState(339);
				qualifiedName();
				}
				break;
			case 14:
				_localctx = new CommentTableContext(_localctx);
				enterOuterAlt(_localctx, 14);
				{
				setState(340);
				match(COMMENT);
				setState(341);
				match(ON);
				setState(342);
				match(TABLE);
				setState(343);
				qualifiedName();
				setState(344);
				match(IS);
				setState(347);
				_errHandler.sync(this);
				switch (_input.LA(1)) {
				case STRING:
				case UNICODE_STRING:
				case ESCAPED_STRING:
					{
					setState(345);
					string();
					}
					break;
				case NULL:
					{
					setState(346);
					match(NULL);
					}
					break;
				default:
					throw new NoViableAltException(this);
				}
				}
				break;
			case 15:
				_localctx = new CommentColumnContext(_localctx);
				enterOuterAlt(_localctx, 15);
				{
				setState(349);
				match(COMMENT);
				setState(350);
				match(ON);
				setState(351);
				match(COLUMN);
				setState(352);
				qualifiedName();
				setState(353);
				match(IS);
				setState(356);
				_errHandler.sync(this);
				switch (_input.LA(1)) {
				case STRING:
				case UNICODE_STRING:
				case ESCAPED_STRING:
					{
					setState(354);
					string();
					}
					break;
				case NULL:
					{
					setState(355);
					match(NULL);
					}
					break;
				default:
					throw new NoViableAltException(this);
				}
				}
				break;
			case 16:
				_localctx = new RenameTableContext(_localctx);
				enterOuterAlt(_localctx, 16);
				{
				setState(358);
				match(ALTER);
				setState(359);
				match(TABLE);
				setState(362);
				_errHandler.sync(this);
				switch ( getInterpreter().adaptivePredict(_input,21,_ctx) ) {
				case 1:
					{
					setState(360);
					match(IF);
					setState(361);
					match(EXISTS);
					}
					break;
				}
				setState(364);
				((RenameTableContext)_localctx).from = qualifiedName();
				setState(365);
				match(RENAME);
				setState(366);
				match(TO);
				setState(367);
				((RenameTableContext)_localctx).to = qualifiedName();
				}
				break;
			case 17:
				_localctx = new AddColumnContext(_localctx);
				enterOuterAlt(_localctx, 17);
				{
				setState(369);
				match(ALTER);
				setState(370);
				match(TABLE);
				setState(373);
				_errHandler.sync(this);
				switch ( getInterpreter().adaptivePredict(_input,22,_ctx) ) {
				case 1:
					{
					setState(371);
					match(IF);
					setState(372);
					match(EXISTS);
					}
					break;
				}
				setState(375);
				((AddColumnContext)_localctx).tableName = qualifiedName();
				setState(376);
				match(ADD);
				setState(377);
				match(COLUMN);
				setState(381);
				_errHandler.sync(this);
				switch ( getInterpreter().adaptivePredict(_input,23,_ctx) ) {
				case 1:
					{
					setState(378);
					match(IF);
					setState(379);
					match(NOT);
					setState(380);
					match(EXISTS);
					}
					break;
				}
				setState(383);
				((AddColumnContext)_localctx).column = columnDefinition();
				}
				break;
			case 18:
				_localctx = new RenameColumnContext(_localctx);
				enterOuterAlt(_localctx, 18);
				{
				setState(385);
				match(ALTER);
				setState(386);
				match(TABLE);
				setState(389);
				_errHandler.sync(this);
				switch ( getInterpreter().adaptivePredict(_input,24,_ctx) ) {
				case 1:
					{
					setState(387);
					match(IF);
					setState(388);
					match(EXISTS);
					}
					break;
				}
				setState(391);
				((RenameColumnContext)_localctx).tableName = qualifiedName();
				setState(392);
				match(RENAME);
				setState(393);
				match(COLUMN);
				setState(396);
				_errHandler.sync(this);
				switch ( getInterpreter().adaptivePredict(_input,25,_ctx) ) {
				case 1:
					{
					setState(394);
					match(IF);
					setState(395);
					match(EXISTS);
					}
					break;
				}
				setState(398);
				((RenameColumnContext)_localctx).from = identifier();
				setState(399);
				match(TO);
				setState(400);
				((RenameColumnContext)_localctx).to = identifier();
				}
				break;
			case 19:
				_localctx = new DropColumnContext(_localctx);
				enterOuterAlt(_localctx, 19);
				{
				setState(402);
				match(ALTER);
				setState(403);
				match(TABLE);
				setState(406);
				_errHandler.sync(this);
				switch ( getInterpreter().adaptivePredict(_input,26,_ctx) ) {
				case 1:
					{
					setState(404);
					match(IF);
					setState(405);
					match(EXISTS);
					}
					break;
				}
				setState(408);
				((DropColumnContext)_localctx).tableName = qualifiedName();
				setState(409);
				match(DROP);
				setState(410);
				match(COLUMN);
				setState(413);
				_errHandler.sync(this);
				switch ( getInterpreter().adaptivePredict(_input,27,_ctx) ) {
				case 1:
					{
					setState(411);
					match(IF);
					setState(412);
					match(EXISTS);
					}
					break;
				}
				setState(415);
				((DropColumnContext)_localctx).column = qualifiedName();
				}
				break;
			case 20:
				_localctx = new SetTableAuthorizationContext(_localctx);
				enterOuterAlt(_localctx, 20);
				{
				setState(417);
				match(ALTER);
				setState(418);
				match(TABLE);
				setState(419);
				((SetTableAuthorizationContext)_localctx).tableName = qualifiedName();
				setState(420);
				match(SET);
				setState(421);
				match(AUTHORIZATION);
				setState(422);
				principal();
				}
				break;
			case 21:
				_localctx = new SetTablePropertiesContext(_localctx);
				enterOuterAlt(_localctx, 21);
				{
				setState(424);
				match(ALTER);
				setState(425);
				match(TABLE);
				setState(426);
				((SetTablePropertiesContext)_localctx).tableName = qualifiedName();
				setState(427);
				match(SET);
				setState(428);
				match(PROPERTIES);
				setState(429);
				propertyAssignments();
				}
				break;
			case 22:
				_localctx = new TableExecuteContext(_localctx);
				enterOuterAlt(_localctx, 22);
				{
				setState(431);
				match(ALTER);
				setState(432);
				match(TABLE);
				setState(433);
				((TableExecuteContext)_localctx).tableName = qualifiedName();
				setState(434);
				match(EXECUTE);
				setState(435);
				((TableExecuteContext)_localctx).procedureName = identifier();
				setState(448);
				_errHandler.sync(this);
				_la = _input.LA(1);
				if (_la==T__1) {
					{
					setState(436);
					match(T__1);
					setState(445);
					_errHandler.sync(this);
					_la = _input.LA(1);
					if ((((_la) & ~0x3f) == 0 && ((1L << _la) & -304556133446578172L) != 0) || ((((_la - 64)) & ~0x3f) == 0 && ((1L << (_la - 64)) & -5424665139366696073L) != 0) || ((((_la - 129)) & ~0x3f) == 0 && ((1L << (_la - 129)) & -1153018536512192553L) != 0) || ((((_la - 193)) & ~0x3f) == 0 && ((1L << (_la - 193)) & -2928466825937175555L) != 0) || ((((_la - 257)) & ~0x3f) == 0 && ((1L << (_la - 257)) & 1133846595561L) != 0)) {
						{
						setState(437);
						callArgument();
						setState(442);
						_errHandler.sync(this);
						_la = _input.LA(1);
						while (_la==T__3) {
							{
							{
							setState(438);
							match(T__3);
							setState(439);
							callArgument();
							}
							}
							setState(444);
							_errHandler.sync(this);
							_la = _input.LA(1);
						}
						}
					}

					setState(447);
					match(T__2);
					}
				}

				setState(452);
				_errHandler.sync(this);
				_la = _input.LA(1);
				if (_la==WHERE) {
					{
					setState(450);
					match(WHERE);
					setState(451);
					((TableExecuteContext)_localctx).where = booleanExpression(0);
					}
				}

				}
				break;
			case 23:
				_localctx = new AnalyzeContext(_localctx);
				enterOuterAlt(_localctx, 23);
				{
				setState(454);
				match(ANALYZE);
				setState(455);
				qualifiedName();
				setState(458);
				_errHandler.sync(this);
				_la = _input.LA(1);
				if (_la==WITH) {
					{
					setState(456);
					match(WITH);
					setState(457);
					properties();
					}
				}

				}
				break;
			case 24:
				_localctx = new CreateMaterializedViewContext(_localctx);
				enterOuterAlt(_localctx, 24);
				{
				setState(460);
				match(CREATE);
				setState(463);
				_errHandler.sync(this);
				_la = _input.LA(1);
				if (_la==OR) {
					{
					setState(461);
					match(OR);
					setState(462);
					match(REPLACE);
					}
				}

				setState(465);
				match(MATERIALIZED);
				setState(466);
				match(VIEW);
				setState(470);
				_errHandler.sync(this);
				switch ( getInterpreter().adaptivePredict(_input,34,_ctx) ) {
				case 1:
					{
					setState(467);
					match(IF);
					setState(468);
					match(NOT);
					setState(469);
					match(EXISTS);
					}
					break;
				}
				setState(472);
				qualifiedName();
				setState(475);
				_errHandler.sync(this);
				_la = _input.LA(1);
				if (_la==COMMENT) {
					{
					setState(473);
					match(COMMENT);
					setState(474);
					string();
					}
				}

				setState(479);
				_errHandler.sync(this);
				_la = _input.LA(1);
				if (_la==WITH) {
					{
					setState(477);
					match(WITH);
					setState(478);
					properties();
					}
				}

				setState(481);
				match(AS);
				setState(482);
				query();
				}
				break;
			case 25:
				_localctx = new CreateViewContext(_localctx);
				enterOuterAlt(_localctx, 25);
				{
				setState(484);
				match(CREATE);
				setState(487);
				_errHandler.sync(this);
				_la = _input.LA(1);
				if (_la==OR) {
					{
					setState(485);
					match(OR);
					setState(486);
					match(REPLACE);
					}
				}

				setState(489);
				match(VIEW);
				setState(490);
				qualifiedName();
				setState(493);
				_errHandler.sync(this);
				_la = _input.LA(1);
				if (_la==COMMENT) {
					{
					setState(491);
					match(COMMENT);
					setState(492);
					string();
					}
				}

				setState(497);
				_errHandler.sync(this);
				_la = _input.LA(1);
				if (_la==SECURITY) {
					{
					setState(495);
					match(SECURITY);
					setState(496);
					_la = _input.LA(1);
					if ( !(_la==DEFINER || _la==INVOKER) ) {
					_errHandler.recoverInline(this);
					}
					else {
						if ( _input.LA(1)==Token.EOF ) matchedEOF = true;
						_errHandler.reportMatch(this);
						consume();
					}
					}
				}

				setState(499);
				match(AS);
				setState(500);
				query();
				}
				break;
			case 26:
				_localctx = new RefreshMaterializedViewContext(_localctx);
				enterOuterAlt(_localctx, 26);
				{
				setState(502);
				match(REFRESH);
				setState(503);
				match(MATERIALIZED);
				setState(504);
				match(VIEW);
				setState(505);
				qualifiedName();
				}
				break;
			case 27:
				_localctx = new DropMaterializedViewContext(_localctx);
				enterOuterAlt(_localctx, 27);
				{
				setState(506);
				match(DROP);
				setState(507);
				match(MATERIALIZED);
				setState(508);
				match(VIEW);
				setState(511);
				_errHandler.sync(this);
				switch ( getInterpreter().adaptivePredict(_input,40,_ctx) ) {
				case 1:
					{
					setState(509);
					match(IF);
					setState(510);
					match(EXISTS);
					}
					break;
				}
				setState(513);
				qualifiedName();
				}
				break;
			case 28:
				_localctx = new RenameMaterializedViewContext(_localctx);
				enterOuterAlt(_localctx, 28);
				{
				setState(514);
				match(ALTER);
				setState(515);
				match(MATERIALIZED);
				setState(516);
				match(VIEW);
				setState(519);
				_errHandler.sync(this);
				switch ( getInterpreter().adaptivePredict(_input,41,_ctx) ) {
				case 1:
					{
					setState(517);
					match(IF);
					setState(518);
					match(EXISTS);
					}
					break;
				}
				setState(521);
				((RenameMaterializedViewContext)_localctx).from = qualifiedName();
				setState(522);
				match(RENAME);
				setState(523);
				match(TO);
				setState(524);
				((RenameMaterializedViewContext)_localctx).to = qualifiedName();
				}
				break;
			case 29:
				_localctx = new SetMaterializedViewPropertiesContext(_localctx);
				enterOuterAlt(_localctx, 29);
				{
				setState(526);
				match(ALTER);
				setState(527);
				match(MATERIALIZED);
				setState(528);
				match(VIEW);
				setState(529);
				qualifiedName();
				setState(530);
				match(SET);
				setState(531);
				match(PROPERTIES);
				setState(532);
				propertyAssignments();
				}
				break;
			case 30:
				_localctx = new DropViewContext(_localctx);
				enterOuterAlt(_localctx, 30);
				{
				setState(534);
				match(DROP);
				setState(535);
				match(VIEW);
				setState(538);
				_errHandler.sync(this);
				switch ( getInterpreter().adaptivePredict(_input,42,_ctx) ) {
				case 1:
					{
					setState(536);
					match(IF);
					setState(537);
					match(EXISTS);
					}
					break;
				}
				setState(540);
				qualifiedName();
				}
				break;
			case 31:
				_localctx = new RenameViewContext(_localctx);
				enterOuterAlt(_localctx, 31);
				{
				setState(541);
				match(ALTER);
				setState(542);
				match(VIEW);
				setState(543);
				((RenameViewContext)_localctx).from = qualifiedName();
				setState(544);
				match(RENAME);
				setState(545);
				match(TO);
				setState(546);
				((RenameViewContext)_localctx).to = qualifiedName();
				}
				break;
			case 32:
				_localctx = new SetViewAuthorizationContext(_localctx);
				enterOuterAlt(_localctx, 32);
				{
				setState(548);
				match(ALTER);
				setState(549);
				match(VIEW);
				setState(550);
				((SetViewAuthorizationContext)_localctx).from = qualifiedName();
				setState(551);
				match(SET);
				setState(552);
				match(AUTHORIZATION);
				setState(553);
				principal();
				}
				break;
			case 33:
				_localctx = new CallContext(_localctx);
				enterOuterAlt(_localctx, 33);
				{
				setState(555);
				match(CALL);
				setState(556);
				qualifiedName();
				setState(557);
				match(T__1);
				setState(566);
				_errHandler.sync(this);
				_la = _input.LA(1);
				if ((((_la) & ~0x3f) == 0 && ((1L << _la) & -304556133446578172L) != 0) || ((((_la - 64)) & ~0x3f) == 0 && ((1L << (_la - 64)) & -5424665139366696073L) != 0) || ((((_la - 129)) & ~0x3f) == 0 && ((1L << (_la - 129)) & -1153018536512192553L) != 0) || ((((_la - 193)) & ~0x3f) == 0 && ((1L << (_la - 193)) & -2928466825937175555L) != 0) || ((((_la - 257)) & ~0x3f) == 0 && ((1L << (_la - 257)) & 1133846595561L) != 0)) {
					{
					setState(558);
					callArgument();
					setState(563);
					_errHandler.sync(this);
					_la = _input.LA(1);
					while (_la==T__3) {
						{
						{
						setState(559);
						match(T__3);
						setState(560);
						callArgument();
						}
						}
						setState(565);
						_errHandler.sync(this);
						_la = _input.LA(1);
					}
					}
				}

				setState(568);
				match(T__2);
				}
				break;
			case 34:
				_localctx = new CreateRoleContext(_localctx);
				enterOuterAlt(_localctx, 34);
				{
				setState(570);
				match(CREATE);
				setState(571);
				match(ROLE);
				setState(572);
				((CreateRoleContext)_localctx).name = identifier();
				setState(576);
				_errHandler.sync(this);
				_la = _input.LA(1);
				if (_la==WITH) {
					{
					setState(573);
					match(WITH);
					setState(574);
					match(ADMIN);
					setState(575);
					grantor();
					}
				}

				setState(580);
				_errHandler.sync(this);
				_la = _input.LA(1);
				if (_la==IN) {
					{
					setState(578);
					match(IN);
					setState(579);
					((CreateRoleContext)_localctx).catalog = identifier();
					}
				}

				}
				break;
			case 35:
				_localctx = new DropRoleContext(_localctx);
				enterOuterAlt(_localctx, 35);
				{
				setState(582);
				match(DROP);
				setState(583);
				match(ROLE);
				setState(584);
				((DropRoleContext)_localctx).name = identifier();
				setState(587);
				_errHandler.sync(this);
				_la = _input.LA(1);
				if (_la==IN) {
					{
					setState(585);
					match(IN);
					setState(586);
					((DropRoleContext)_localctx).catalog = identifier();
					}
				}

				}
				break;
			case 36:
				_localctx = new GrantRolesContext(_localctx);
				enterOuterAlt(_localctx, 36);
				{
				setState(589);
				match(GRANT);
				setState(590);
				roles();
				setState(591);
				match(TO);
				setState(592);
				principal();
				setState(597);
				_errHandler.sync(this);
				_la = _input.LA(1);
				while (_la==T__3) {
					{
					{
					setState(593);
					match(T__3);
					setState(594);
					principal();
					}
					}
					setState(599);
					_errHandler.sync(this);
					_la = _input.LA(1);
				}
				setState(603);
				_errHandler.sync(this);
				_la = _input.LA(1);
				if (_la==WITH) {
					{
					setState(600);
					match(WITH);
					setState(601);
					match(ADMIN);
					setState(602);
					match(OPTION);
					}
				}

				setState(608);
				_errHandler.sync(this);
				_la = _input.LA(1);
				if (_la==GRANTED) {
					{
					setState(605);
					match(GRANTED);
					setState(606);
					match(BY);
					setState(607);
					grantor();
					}
				}

				setState(612);
				_errHandler.sync(this);
				_la = _input.LA(1);
				if (_la==IN) {
					{
					setState(610);
					match(IN);
					setState(611);
					((GrantRolesContext)_localctx).catalog = identifier();
					}
				}

				}
				break;
			case 37:
				_localctx = new RevokeRolesContext(_localctx);
				enterOuterAlt(_localctx, 37);
				{
				setState(614);
				match(REVOKE);
				setState(618);
				_errHandler.sync(this);
				switch ( getInterpreter().adaptivePredict(_input,52,_ctx) ) {
				case 1:
					{
					setState(615);
					match(ADMIN);
					setState(616);
					match(OPTION);
					setState(617);
					match(FOR);
					}
					break;
				}
				setState(620);
				roles();
				setState(621);
				match(FROM);
				setState(622);
				principal();
				setState(627);
				_errHandler.sync(this);
				_la = _input.LA(1);
				while (_la==T__3) {
					{
					{
					setState(623);
					match(T__3);
					setState(624);
					principal();
					}
					}
					setState(629);
					_errHandler.sync(this);
					_la = _input.LA(1);
				}
				setState(633);
				_errHandler.sync(this);
				_la = _input.LA(1);
				if (_la==GRANTED) {
					{
					setState(630);
					match(GRANTED);
					setState(631);
					match(BY);
					setState(632);
					grantor();
					}
				}

				setState(637);
				_errHandler.sync(this);
				_la = _input.LA(1);
				if (_la==IN) {
					{
					setState(635);
					match(IN);
					setState(636);
					((RevokeRolesContext)_localctx).catalog = identifier();
					}
				}

				}
				break;
			case 38:
				_localctx = new SetRoleContext(_localctx);
				enterOuterAlt(_localctx, 38);
				{
				setState(639);
				match(SET);
				setState(640);
				match(ROLE);
				setState(644);
				_errHandler.sync(this);
				switch ( getInterpreter().adaptivePredict(_input,56,_ctx) ) {
				case 1:
					{
					setState(641);
					match(ALL);
					}
					break;
				case 2:
					{
					setState(642);
					match(NONE);
					}
					break;
				case 3:
					{
					setState(643);
					((SetRoleContext)_localctx).role = identifier();
					}
					break;
				}
				setState(648);
				_errHandler.sync(this);
				_la = _input.LA(1);
				if (_la==IN) {
					{
					setState(646);
					match(IN);
					setState(647);
					((SetRoleContext)_localctx).catalog = identifier();
					}
				}

				}
				break;
			case 39:
				_localctx = new GrantContext(_localctx);
				enterOuterAlt(_localctx, 39);
				{
				setState(650);
				match(GRANT);
				setState(661);
				_errHandler.sync(this);
				switch (_input.LA(1)) {
				case CREATE:
				case DELETE:
				case INSERT:
				case SELECT:
				case UPDATE:
					{
					setState(651);
					privilege();
					setState(656);
					_errHandler.sync(this);
					_la = _input.LA(1);
					while (_la==T__3) {
						{
						{
						setState(652);
						match(T__3);
						setState(653);
						privilege();
						}
						}
						setState(658);
						_errHandler.sync(this);
						_la = _input.LA(1);
					}
					}
					break;
				case ALL:
					{
					setState(659);
					match(ALL);
					setState(660);
					match(PRIVILEGES);
					}
					break;
				default:
					throw new NoViableAltException(this);
				}
				setState(663);
				match(ON);
				setState(665);
				_errHandler.sync(this);
				switch ( getInterpreter().adaptivePredict(_input,60,_ctx) ) {
				case 1:
					{
					setState(664);
					_la = _input.LA(1);
					if ( !(_la==SCHEMA || _la==TABLE) ) {
					_errHandler.recoverInline(this);
					}
					else {
						if ( _input.LA(1)==Token.EOF ) matchedEOF = true;
						_errHandler.reportMatch(this);
						consume();
					}
					}
					break;
				}
				setState(667);
				qualifiedName();
				setState(668);
				match(TO);
				setState(669);
				((GrantContext)_localctx).grantee = principal();
				setState(673);
				_errHandler.sync(this);
				_la = _input.LA(1);
				if (_la==WITH) {
					{
					setState(670);
					match(WITH);
					setState(671);
					match(GRANT);
					setState(672);
					match(OPTION);
					}
				}

				}
				break;
			case 40:
				_localctx = new DenyContext(_localctx);
				enterOuterAlt(_localctx, 40);
				{
				setState(675);
				match(DENY);
				setState(686);
				_errHandler.sync(this);
				switch (_input.LA(1)) {
				case CREATE:
				case DELETE:
				case INSERT:
				case SELECT:
				case UPDATE:
					{
					setState(676);
					privilege();
					setState(681);
					_errHandler.sync(this);
					_la = _input.LA(1);
					while (_la==T__3) {
						{
						{
						setState(677);
						match(T__3);
						setState(678);
						privilege();
						}
						}
						setState(683);
						_errHandler.sync(this);
						_la = _input.LA(1);
					}
					}
					break;
				case ALL:
					{
					setState(684);
					match(ALL);
					setState(685);
					match(PRIVILEGES);
					}
					break;
				default:
					throw new NoViableAltException(this);
				}
				setState(688);
				match(ON);
				setState(690);
				_errHandler.sync(this);
				switch ( getInterpreter().adaptivePredict(_input,64,_ctx) ) {
				case 1:
					{
					setState(689);
					_la = _input.LA(1);
					if ( !(_la==SCHEMA || _la==TABLE) ) {
					_errHandler.recoverInline(this);
					}
					else {
						if ( _input.LA(1)==Token.EOF ) matchedEOF = true;
						_errHandler.reportMatch(this);
						consume();
					}
					}
					break;
				}
				setState(692);
				qualifiedName();
				setState(693);
				match(TO);
				setState(694);
				((DenyContext)_localctx).grantee = principal();
				}
				break;
			case 41:
				_localctx = new RevokeContext(_localctx);
				enterOuterAlt(_localctx, 41);
				{
				setState(696);
				match(REVOKE);
				setState(700);
				_errHandler.sync(this);
				_la = _input.LA(1);
				if (_la==GRANT) {
					{
					setState(697);
					match(GRANT);
					setState(698);
					match(OPTION);
					setState(699);
					match(FOR);
					}
				}

				setState(712);
				_errHandler.sync(this);
				switch (_input.LA(1)) {
				case CREATE:
				case DELETE:
				case INSERT:
				case SELECT:
				case UPDATE:
					{
					setState(702);
					privilege();
					setState(707);
					_errHandler.sync(this);
					_la = _input.LA(1);
					while (_la==T__3) {
						{
						{
						setState(703);
						match(T__3);
						setState(704);
						privilege();
						}
						}
						setState(709);
						_errHandler.sync(this);
						_la = _input.LA(1);
					}
					}
					break;
				case ALL:
					{
					setState(710);
					match(ALL);
					setState(711);
					match(PRIVILEGES);
					}
					break;
				default:
					throw new NoViableAltException(this);
				}
				setState(714);
				match(ON);
				setState(716);
				_errHandler.sync(this);
				switch ( getInterpreter().adaptivePredict(_input,68,_ctx) ) {
				case 1:
					{
					setState(715);
					_la = _input.LA(1);
					if ( !(_la==SCHEMA || _la==TABLE) ) {
					_errHandler.recoverInline(this);
					}
					else {
						if ( _input.LA(1)==Token.EOF ) matchedEOF = true;
						_errHandler.reportMatch(this);
						consume();
					}
					}
					break;
				}
				setState(718);
				qualifiedName();
				setState(719);
				match(FROM);
				setState(720);
				((RevokeContext)_localctx).grantee = principal();
				}
				break;
			case 42:
				_localctx = new ShowGrantsContext(_localctx);
				enterOuterAlt(_localctx, 42);
				{
				setState(722);
				match(SHOW);
				setState(723);
				match(GRANTS);
				setState(729);
				_errHandler.sync(this);
				_la = _input.LA(1);
				if (_la==ON) {
					{
					setState(724);
					match(ON);
					setState(726);
					_errHandler.sync(this);
					_la = _input.LA(1);
					if (_la==TABLE) {
						{
						setState(725);
						match(TABLE);
						}
					}

					setState(728);
					qualifiedName();
					}
				}

				}
				break;
			case 43:
				_localctx = new ExplainContext(_localctx);
				enterOuterAlt(_localctx, 43);
				{
				setState(731);
				match(EXPLAIN);
				setState(743);
				_errHandler.sync(this);
				switch ( getInterpreter().adaptivePredict(_input,72,_ctx) ) {
				case 1:
					{
					setState(732);
					match(T__1);
					setState(733);
					explainOption();
					setState(738);
					_errHandler.sync(this);
					_la = _input.LA(1);
					while (_la==T__3) {
						{
						{
						setState(734);
						match(T__3);
						setState(735);
						explainOption();
						}
						}
						setState(740);
						_errHandler.sync(this);
						_la = _input.LA(1);
					}
					setState(741);
					match(T__2);
					}
					break;
				}
				setState(745);
				statement();
				}
				break;
			case 44:
				_localctx = new ExplainAnalyzeContext(_localctx);
				enterOuterAlt(_localctx, 44);
				{
				setState(746);
				match(EXPLAIN);
				setState(747);
				match(ANALYZE);
				setState(749);
				_errHandler.sync(this);
				_la = _input.LA(1);
				if (_la==VERBOSE) {
					{
					setState(748);
					match(VERBOSE);
					}
				}

				setState(751);
				statement();
				}
				break;
			case 45:
				_localctx = new ShowCreateTableContext(_localctx);
				enterOuterAlt(_localctx, 45);
				{
				setState(752);
				match(SHOW);
				setState(753);
				match(CREATE);
				setState(754);
				match(TABLE);
				setState(755);
				qualifiedName();
				}
				break;
			case 46:
				_localctx = new ShowCreateSchemaContext(_localctx);
				enterOuterAlt(_localctx, 46);
				{
				setState(756);
				match(SHOW);
				setState(757);
				match(CREATE);
				setState(758);
				match(SCHEMA);
				setState(759);
				qualifiedName();
				}
				break;
			case 47:
				_localctx = new ShowCreateViewContext(_localctx);
				enterOuterAlt(_localctx, 47);
				{
				setState(760);
				match(SHOW);
				setState(761);
				match(CREATE);
				setState(762);
				match(VIEW);
				setState(763);
				qualifiedName();
				}
				break;
			case 48:
				_localctx = new ShowCreateMaterializedViewContext(_localctx);
				enterOuterAlt(_localctx, 48);
				{
				setState(764);
				match(SHOW);
				setState(765);
				match(CREATE);
				setState(766);
				match(MATERIALIZED);
				setState(767);
				match(VIEW);
				setState(768);
				qualifiedName();
				}
				break;
			case 49:
				_localctx = new ShowTablesContext(_localctx);
				enterOuterAlt(_localctx, 49);
				{
				setState(769);
				match(SHOW);
				setState(770);
				match(TABLES);
				setState(773);
				_errHandler.sync(this);
				_la = _input.LA(1);
				if (_la==FROM || _la==IN) {
					{
					setState(771);
					_la = _input.LA(1);
					if ( !(_la==FROM || _la==IN) ) {
					_errHandler.recoverInline(this);
					}
					else {
						if ( _input.LA(1)==Token.EOF ) matchedEOF = true;
						_errHandler.reportMatch(this);
						consume();
					}
					setState(772);
					qualifiedName();
					}
				}

				setState(781);
				_errHandler.sync(this);
				_la = _input.LA(1);
				if (_la==LIKE) {
					{
					setState(775);
					match(LIKE);
					setState(776);
					((ShowTablesContext)_localctx).pattern = string();
					setState(779);
					_errHandler.sync(this);
					_la = _input.LA(1);
					if (_la==ESCAPE) {
						{
						setState(777);
						match(ESCAPE);
						setState(778);
						((ShowTablesContext)_localctx).escape = string();
						}
					}

					}
				}

				}
				break;
			case 50:
				_localctx = new ShowSchemasContext(_localctx);
				enterOuterAlt(_localctx, 50);
				{
				setState(783);
				match(SHOW);
				setState(784);
				match(SCHEMAS);
				setState(787);
				_errHandler.sync(this);
				_la = _input.LA(1);
				if (_la==FROM || _la==IN) {
					{
					setState(785);
					_la = _input.LA(1);
					if ( !(_la==FROM || _la==IN) ) {
					_errHandler.recoverInline(this);
					}
					else {
						if ( _input.LA(1)==Token.EOF ) matchedEOF = true;
						_errHandler.reportMatch(this);
						consume();
					}
					setState(786);
					identifier();
					}
				}

				setState(795);
				_errHandler.sync(this);
				_la = _input.LA(1);
				if (_la==LIKE) {
					{
					setState(789);
					match(LIKE);
					setState(790);
					((ShowSchemasContext)_localctx).pattern = string();
					setState(793);
					_errHandler.sync(this);
					_la = _input.LA(1);
					if (_la==ESCAPE) {
						{
						setState(791);
						match(ESCAPE);
						setState(792);
						((ShowSchemasContext)_localctx).escape = string();
						}
					}

					}
				}

				}
				break;
			case 51:
				_localctx = new ShowCatalogsContext(_localctx);
				enterOuterAlt(_localctx, 51);
				{
				setState(797);
				match(SHOW);
				setState(798);
				match(CATALOGS);
				setState(805);
				_errHandler.sync(this);
				_la = _input.LA(1);
				if (_la==LIKE) {
					{
					setState(799);
					match(LIKE);
					setState(800);
					((ShowCatalogsContext)_localctx).pattern = string();
					setState(803);
					_errHandler.sync(this);
					_la = _input.LA(1);
					if (_la==ESCAPE) {
						{
						setState(801);
						match(ESCAPE);
						setState(802);
						((ShowCatalogsContext)_localctx).escape = string();
						}
					}

					}
				}

				}
				break;
			case 52:
				_localctx = new ShowColumnsContext(_localctx);
				enterOuterAlt(_localctx, 52);
				{
				setState(807);
				match(SHOW);
				setState(808);
				match(COLUMNS);
				setState(809);
				_la = _input.LA(1);
				if ( !(_la==FROM || _la==IN) ) {
				_errHandler.recoverInline(this);
				}
				else {
					if ( _input.LA(1)==Token.EOF ) matchedEOF = true;
					_errHandler.reportMatch(this);
					consume();
				}
				setState(811);
				_errHandler.sync(this);
				_la = _input.LA(1);
				if ((((_la) & ~0x3f) == 0 && ((1L << _la) & -9203672295665565696L) != 0) || ((((_la - 64)) & ~0x3f) == 0 && ((1L << (_la - 64)) & -5424682731988948105L) != 0) || ((((_la - 129)) & ~0x3f) == 0 && ((1L << (_la - 129)) & -1153018544028386985L) != 0) || ((((_la - 193)) & ~0x3f) == 0 && ((1L << (_la - 193)) & -2928537194681353219L) != 0) || ((((_la - 257)) & ~0x3f) == 0 && ((1L << (_la - 257)) & 32212256745L) != 0)) {
					{
					setState(810);
					qualifiedName();
					}
				}

				setState(819);
				_errHandler.sync(this);
				_la = _input.LA(1);
				if (_la==LIKE) {
					{
					setState(813);
					match(LIKE);
					setState(814);
					((ShowColumnsContext)_localctx).pattern = string();
					setState(817);
					_errHandler.sync(this);
					_la = _input.LA(1);
					if (_la==ESCAPE) {
						{
						setState(815);
						match(ESCAPE);
						setState(816);
						((ShowColumnsContext)_localctx).escape = string();
						}
					}

					}
				}

				}
				break;
			case 53:
				_localctx = new ShowStatsContext(_localctx);
				enterOuterAlt(_localctx, 53);
				{
				setState(821);
				match(SHOW);
				setState(822);
				match(STATS);
				setState(823);
				match(FOR);
				setState(824);
				qualifiedName();
				}
				break;
			case 54:
				_localctx = new ShowStatsForQueryContext(_localctx);
				enterOuterAlt(_localctx, 54);
				{
				setState(825);
				match(SHOW);
				setState(826);
				match(STATS);
				setState(827);
				match(FOR);
				setState(828);
				match(T__1);
				setState(829);
				query();
				setState(830);
				match(T__2);
				}
				break;
			case 55:
				_localctx = new ShowRolesContext(_localctx);
				enterOuterAlt(_localctx, 55);
				{
				setState(832);
				match(SHOW);
				setState(834);
				_errHandler.sync(this);
				_la = _input.LA(1);
				if (_la==CURRENT) {
					{
					setState(833);
					match(CURRENT);
					}
				}

				setState(836);
				match(ROLES);
				setState(839);
				_errHandler.sync(this);
				_la = _input.LA(1);
				if (_la==FROM || _la==IN) {
					{
					setState(837);
					_la = _input.LA(1);
					if ( !(_la==FROM || _la==IN) ) {
					_errHandler.recoverInline(this);
					}
					else {
						if ( _input.LA(1)==Token.EOF ) matchedEOF = true;
						_errHandler.reportMatch(this);
						consume();
					}
					setState(838);
					identifier();
					}
				}

				}
				break;
			case 56:
				_localctx = new ShowRoleGrantsContext(_localctx);
				enterOuterAlt(_localctx, 56);
				{
				setState(841);
				match(SHOW);
				setState(842);
				match(ROLE);
				setState(843);
				match(GRANTS);
				setState(846);
				_errHandler.sync(this);
				_la = _input.LA(1);
				if (_la==FROM || _la==IN) {
					{
					setState(844);
					_la = _input.LA(1);
					if ( !(_la==FROM || _la==IN) ) {
					_errHandler.recoverInline(this);
					}
					else {
						if ( _input.LA(1)==Token.EOF ) matchedEOF = true;
						_errHandler.reportMatch(this);
						consume();
					}
					setState(845);
					identifier();
					}
				}

				}
				break;
			case 57:
				_localctx = new ShowColumnsContext(_localctx);
				enterOuterAlt(_localctx, 57);
				{
				setState(848);
				match(DESCRIBE);
				setState(849);
				qualifiedName();
				}
				break;
			case 58:
				_localctx = new ShowColumnsContext(_localctx);
				enterOuterAlt(_localctx, 58);
				{
				setState(850);
				match(DESC);
				setState(851);
				qualifiedName();
				}
				break;
			case 59:
				_localctx = new ShowFunctionsContext(_localctx);
				enterOuterAlt(_localctx, 59);
				{
				setState(852);
				match(SHOW);
				setState(853);
				match(FUNCTIONS);
				setState(860);
				_errHandler.sync(this);
				_la = _input.LA(1);
				if (_la==LIKE) {
					{
					setState(854);
					match(LIKE);
					setState(855);
					((ShowFunctionsContext)_localctx).pattern = string();
					setState(858);
					_errHandler.sync(this);
					_la = _input.LA(1);
					if (_la==ESCAPE) {
						{
						setState(856);
						match(ESCAPE);
						setState(857);
						((ShowFunctionsContext)_localctx).escape = string();
						}
					}

					}
				}

				}
				break;
			case 60:
				_localctx = new ShowSessionContext(_localctx);
				enterOuterAlt(_localctx, 60);
				{
				setState(862);
				match(SHOW);
				setState(863);
				match(SESSION);
				setState(870);
				_errHandler.sync(this);
				_la = _input.LA(1);
				if (_la==LIKE) {
					{
					setState(864);
					match(LIKE);
					setState(865);
					((ShowSessionContext)_localctx).pattern = string();
					setState(868);
					_errHandler.sync(this);
					_la = _input.LA(1);
					if (_la==ESCAPE) {
						{
						setState(866);
						match(ESCAPE);
						setState(867);
						((ShowSessionContext)_localctx).escape = string();
						}
					}

					}
				}

				}
				break;
			case 61:
				_localctx = new SetSessionContext(_localctx);
				enterOuterAlt(_localctx, 61);
				{
				setState(872);
				match(SET);
				setState(873);
				match(SESSION);
				setState(874);
				qualifiedName();
				setState(875);
				match(EQ);
				setState(876);
				expression();
				}
				break;
			case 62:
				_localctx = new ResetSessionContext(_localctx);
				enterOuterAlt(_localctx, 62);
				{
				setState(878);
				match(RESET);
				setState(879);
				match(SESSION);
				setState(880);
				qualifiedName();
				}
				break;
			case 63:
				_localctx = new StartTransactionContext(_localctx);
				enterOuterAlt(_localctx, 63);
				{
				setState(881);
				match(START);
				setState(882);
				match(TRANSACTION);
				setState(891);
				_errHandler.sync(this);
				_la = _input.LA(1);
				if (_la==ISOLATION || _la==READ) {
					{
					setState(883);
					transactionMode();
					setState(888);
					_errHandler.sync(this);
					_la = _input.LA(1);
					while (_la==T__3) {
						{
						{
						setState(884);
						match(T__3);
						setState(885);
						transactionMode();
						}
						}
						setState(890);
						_errHandler.sync(this);
						_la = _input.LA(1);
					}
					}
				}

				}
				break;
			case 64:
				_localctx = new CommitContext(_localctx);
				enterOuterAlt(_localctx, 64);
				{
				setState(893);
				match(COMMIT);
				setState(895);
				_errHandler.sync(this);
				_la = _input.LA(1);
				if (_la==WORK) {
					{
					setState(894);
					match(WORK);
					}
				}

				}
				break;
			case 65:
				_localctx = new RollbackContext(_localctx);
				enterOuterAlt(_localctx, 65);
				{
				setState(897);
				match(ROLLBACK);
				setState(899);
				_errHandler.sync(this);
				_la = _input.LA(1);
				if (_la==WORK) {
					{
					setState(898);
					match(WORK);
					}
				}

				}
				break;
			case 66:
				_localctx = new PrepareContext(_localctx);
				enterOuterAlt(_localctx, 66);
				{
				setState(901);
				match(PREPARE);
				setState(902);
				identifier();
				setState(903);
				match(FROM);
				setState(904);
				statement();
				}
				break;
			case 67:
				_localctx = new DeallocateContext(_localctx);
				enterOuterAlt(_localctx, 67);
				{
				setState(906);
				match(DEALLOCATE);
				setState(907);
				match(PREPARE);
				setState(908);
				identifier();
				}
				break;
			case 68:
				_localctx = new ExecuteContext(_localctx);
				enterOuterAlt(_localctx, 68);
				{
				setState(909);
				match(EXECUTE);
				setState(910);
				identifier();
				setState(920);
				_errHandler.sync(this);
				_la = _input.LA(1);
				if (_la==USING) {
					{
					setState(911);
					match(USING);
					setState(912);
					expression();
					setState(917);
					_errHandler.sync(this);
					_la = _input.LA(1);
					while (_la==T__3) {
						{
						{
						setState(913);
						match(T__3);
						setState(914);
						expression();
						}
						}
						setState(919);
						_errHandler.sync(this);
						_la = _input.LA(1);
					}
					}
				}

				}
				break;
			case 69:
				_localctx = new DescribeInputContext(_localctx);
				enterOuterAlt(_localctx, 69);
				{
				setState(922);
				match(DESCRIBE);
				setState(923);
				match(INPUT);
				setState(924);
				identifier();
				}
				break;
			case 70:
				_localctx = new DescribeOutputContext(_localctx);
				enterOuterAlt(_localctx, 70);
				{
				setState(925);
				match(DESCRIBE);
				setState(926);
				match(OUTPUT);
				setState(927);
				identifier();
				}
				break;
			case 71:
				_localctx = new SetPathContext(_localctx);
				enterOuterAlt(_localctx, 71);
				{
				setState(928);
				match(SET);
				setState(929);
				match(PATH);
				setState(930);
				pathSpecification();
				}
				break;
			case 72:
				_localctx = new SetTimeZoneContext(_localctx);
				enterOuterAlt(_localctx, 72);
				{
				setState(931);
				match(SET);
				setState(932);
				match(TIME);
				setState(933);
				match(ZONE);
				setState(936);
				_errHandler.sync(this);
				switch ( getInterpreter().adaptivePredict(_input,98,_ctx) ) {
				case 1:
					{
					setState(934);
					match(LOCAL);
					}
					break;
				case 2:
					{
					setState(935);
					expression();
					}
					break;
				}
				}
				break;
			case 73:
				_localctx = new UpdateContext(_localctx);
				enterOuterAlt(_localctx, 73);
				{
				setState(938);
				match(UPDATE);
				setState(939);
				qualifiedName();
				setState(940);
				match(SET);
				setState(941);
				updateAssignment();
				setState(946);
				_errHandler.sync(this);
				_la = _input.LA(1);
				while (_la==T__3) {
					{
					{
					setState(942);
					match(T__3);
					setState(943);
					updateAssignment();
					}
					}
					setState(948);
					_errHandler.sync(this);
					_la = _input.LA(1);
				}
				setState(951);
				_errHandler.sync(this);
				_la = _input.LA(1);
				if (_la==WHERE) {
					{
					setState(949);
					match(WHERE);
					setState(950);
					((UpdateContext)_localctx).where = booleanExpression(0);
					}
				}

				}
				break;
			case 74:
				_localctx = new MergeContext(_localctx);
				enterOuterAlt(_localctx, 74);
				{
				setState(953);
				match(MERGE);
				setState(954);
				match(INTO);
				setState(955);
				qualifiedName();
				setState(960);
				_errHandler.sync(this);
				_la = _input.LA(1);
				if ((((_la) & ~0x3f) == 0 && ((1L << _la) & -9203672293518082048L) != 0) || ((((_la - 64)) & ~0x3f) == 0 && ((1L << (_la - 64)) & -5424682731988948105L) != 0) || ((((_la - 129)) & ~0x3f) == 0 && ((1L << (_la - 129)) & -1153018544028386985L) != 0) || ((((_la - 193)) & ~0x3f) == 0 && ((1L << (_la - 193)) & -2928537194681353219L) != 0) || ((((_la - 257)) & ~0x3f) == 0 && ((1L << (_la - 257)) & 32212256745L) != 0)) {
					{
					setState(957);
					_errHandler.sync(this);
					_la = _input.LA(1);
					if (_la==AS) {
						{
						setState(956);
						match(AS);
						}
					}

					setState(959);
					identifier();
					}
				}

				setState(962);
				match(USING);
				setState(963);
				relation(0);
				setState(964);
				match(ON);
				setState(965);
				expression();
				setState(967); 
				_errHandler.sync(this);
				_la = _input.LA(1);
				do {
					{
					{
					setState(966);
					mergeCase();
					}
					}
					setState(969); 
					_errHandler.sync(this);
					_la = _input.LA(1);
				} while ( _la==WHEN );
				}
				break;
			case 75:
				_localctx = new DeclareCursorContext(_localctx);
				enterOuterAlt(_localctx, 75);
				{
				setState(971);
				match(DECLARE);
				setState(972);
				((DeclareCursorContext)_localctx).name = identifier();
				setState(974);
				_errHandler.sync(this);
				_la = _input.LA(1);
				if (_la==T__4) {
					{
					setState(973);
					match(T__4);
					}
				}

				setState(977);
				_errHandler.sync(this);
				_la = _input.LA(1);
				if (_la==T__5 || _la==T__6) {
					{
					setState(976);
					_la = _input.LA(1);
					if ( !(_la==T__5 || _la==T__6) ) {
					_errHandler.recoverInline(this);
					}
					else {
						if ( _input.LA(1)==Token.EOF ) matchedEOF = true;
						_errHandler.reportMatch(this);
						consume();
					}
					}
				}

				setState(983);
				_errHandler.sync(this);
				_la = _input.LA(1);
				if (_la==T__7 || _la==NO) {
					{
					setState(980);
					_errHandler.sync(this);
					_la = _input.LA(1);
					if (_la==NO) {
						{
						setState(979);
						match(NO);
						}
					}

					setState(982);
					match(T__7);
					}
				}

				setState(985);
				match(CURSOR);
				setState(988);
				_errHandler.sync(this);
				_la = _input.LA(1);
				if (_la==WITH || _la==WITHOUT) {
					{
					setState(986);
					_la = _input.LA(1);
					if ( !(_la==WITH || _la==WITHOUT) ) {
					_errHandler.recoverInline(this);
					}
					else {
						if ( _input.LA(1)==Token.EOF ) matchedEOF = true;
						_errHandler.reportMatch(this);
						consume();
					}
					setState(987);
					match(T__8);
					}
				}

				setState(990);
				match(FOR);
				setState(991);
				((DeclareCursorContext)_localctx).body = query();
				}
				break;
			case 76:
				_localctx = new FetchCursorContext(_localctx);
				enterOuterAlt(_localctx, 76);
				{
				setState(993);
				match(FETCH);
				setState(994);
				((FetchCursorContext)_localctx).row = match(INTEGER_VALUE);
				setState(995);
				_la = _input.LA(1);
				if ( !(_la==FROM || _la==IN) ) {
				_errHandler.recoverInline(this);
				}
				else {
					if ( _input.LA(1)==Token.EOF ) matchedEOF = true;
					_errHandler.reportMatch(this);
					consume();
				}
				setState(996);
				((FetchCursorContext)_localctx).cursor = identifier();
				}
				break;
			case 77:
				_localctx = new ImpersonateUserContext(_localctx);
				enterOuterAlt(_localctx, 77);
				{
				setState(997);
				match(IMPERSONATE);
				setState(998);
				expression();
				}
				break;
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
	public static class QueryContext extends ParserRuleContext {
		public QueryNoWithContext queryNoWith() {
			return getRuleContext(QueryNoWithContext.class,0);
		}
		public WithContext with() {
			return getRuleContext(WithContext.class,0);
		}
		public QueryContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_query; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterQuery(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitQuery(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitQuery(this);
			else return visitor.visitChildren(this);
		}
	}

	public final QueryContext query() throws RecognitionException {
		QueryContext _localctx = new QueryContext(_ctx, getState());
		enterRule(_localctx, 12, RULE_query);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(1002);
			_errHandler.sync(this);
			_la = _input.LA(1);
			if (_la==WITH) {
				{
				setState(1001);
				with();
				}
			}

			setState(1004);
			queryNoWith();
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
	public static class WithContext extends ParserRuleContext {
		public TerminalNode WITH() { return getToken(SqlBaseParser.WITH, 0); }
		public List<NamedQueryContext> namedQuery() {
			return getRuleContexts(NamedQueryContext.class);
		}
		public NamedQueryContext namedQuery(int i) {
			return getRuleContext(NamedQueryContext.class,i);
		}
		public TerminalNode RECURSIVE() { return getToken(SqlBaseParser.RECURSIVE, 0); }
		public WithContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_with; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterWith(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitWith(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitWith(this);
			else return visitor.visitChildren(this);
		}
	}

	public final WithContext with() throws RecognitionException {
		WithContext _localctx = new WithContext(_ctx, getState());
		enterRule(_localctx, 14, RULE_with);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(1006);
			match(WITH);
			setState(1008);
			_errHandler.sync(this);
			_la = _input.LA(1);
			if (_la==RECURSIVE) {
				{
				setState(1007);
				match(RECURSIVE);
				}
			}

			setState(1010);
			namedQuery();
			setState(1015);
			_errHandler.sync(this);
			_la = _input.LA(1);
			while (_la==T__3) {
				{
				{
				setState(1011);
				match(T__3);
				setState(1012);
				namedQuery();
				}
				}
				setState(1017);
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
	public static class TableElementContext extends ParserRuleContext {
		public ColumnDefinitionContext columnDefinition() {
			return getRuleContext(ColumnDefinitionContext.class,0);
		}
		public LikeClauseContext likeClause() {
			return getRuleContext(LikeClauseContext.class,0);
		}
		public TableElementContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_tableElement; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterTableElement(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitTableElement(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitTableElement(this);
			else return visitor.visitChildren(this);
		}
	}

	public final TableElementContext tableElement() throws RecognitionException {
		TableElementContext _localctx = new TableElementContext(_ctx, getState());
		enterRule(_localctx, 16, RULE_tableElement);
		try {
			setState(1020);
			_errHandler.sync(this);
			switch (_input.LA(1)) {
			case ADD:
			case ADMIN:
			case AFTER:
			case ALL:
			case ANALYZE:
			case ANY:
			case ARRAY:
			case ASC:
			case AT:
			case AUTHORIZATION:
			case BERNOULLI:
			case CALL:
			case CASCADE:
			case CATALOGS:
			case COLLATE:
			case COLUMN:
			case COLUMNS:
			case COMMENT:
			case COMMIT:
			case COMMITTED:
			case COUNT:
			case CURRENT:
			case CURSOR:
			case DATA:
			case DATE:
			case DAY:
			case DECLARE:
			case DEFAULT:
			case DEFINER:
			case DENY:
			case DESC:
			case DEFINE:
			case DISTRIBUTED:
			case DOUBLE:
			case EMPTY:
			case EPOCH:
			case ERROR:
			case EXCLUDING:
			case EXPLAIN:
			case FETCH:
			case FILTER:
			case FINAL:
			case FIRST:
			case FOLLOWING:
			case FORMAT:
			case FUNCTIONS:
			case GRANT:
			case GRANTED:
			case GRANTS:
			case GRAPHVIZ:
			case GROUPS:
			case HOUR:
			case IF:
			case IGNORE:
			case IMPERSONATE:
			case INCLUDING:
			case INITIAL:
			case INPUT:
			case INTERVAL:
			case INVOKER:
			case IO:
			case ISOLATION:
			case JSON:
			case LAST:
			case LATERAL:
			case LEVEL:
			case LIMIT:
			case LOCAL:
			case LOGICAL:
			case MAP:
			case MATCH:
			case MATCHED:
			case MATCHES:
			case MATCH_RECOGNIZE:
			case MATERIALIZED:
			case MEASURES:
			case MERGE:
			case MINUTE:
			case MONTH:
			case NEXT:
			case NFC:
			case NFD:
			case NFKC:
			case NFKD:
			case NO:
			case NONE:
			case NULLIF:
			case NULLS:
			case OFFSET:
			case OMIT:
			case OF:
			case ONE:
			case ONLY:
			case OPERATOR:
			case OPTION:
			case ORDINALITY:
			case OUTPUT:
			case OVER:
			case OVERFLOW:
			case PARTITION:
			case PARTITIONS:
			case PAST:
			case PATH:
			case PATTERN:
			case PER:
			case PERMUTE:
			case POSITION:
			case PRECEDING:
			case PRECISION:
			case PRIVILEGES:
			case PROPERTIES:
			case RANGE:
			case READ:
			case REFRESH:
			case RENAME:
			case REPEATABLE:
			case REPLACE:
			case RESET:
			case RESPECT:
			case RESTRICT:
			case REVOKE:
			case ROLE:
			case ROLES:
			case ROLLBACK:
			case ROW:
			case ROWS:
			case RUNNING:
			case SCHEMA:
			case SCHEMAS:
			case SECOND:
			case SECURITY:
			case SEEK:
			case SERIALIZABLE:
			case SESSION:
			case SESSION_USER:
			case SET:
			case SETS:
			case SHOW:
			case SOME:
			case START:
			case STATS:
			case SUBSET:
			case SUBSTRING:
			case SYSTEM:
			case TABLES:
			case TABLESAMPLE:
			case TEXT:
			case TIES:
			case TIME:
			case TIMESTAMP:
			case TO:
			case TRANSACTION:
			case TRUNCATE:
			case TRY_CAST:
			case TYPE:
			case UNBOUNDED:
			case UNCOMMITTED:
			case UNMATCHED:
			case UPDATE:
			case USE:
			case USER:
			case VALIDATE:
			case VERBOSE:
			case VERSION:
			case VIEW:
			case WINDOW:
			case WITHIN:
			case WITHOUT:
			case WORK:
			case WRITE:
			case YEAR:
			case ZONE:
			case IDENTIFIER:
			case DIGIT_IDENTIFIER:
			case QUOTED_IDENTIFIER:
			case BACKQUOTED_IDENTIFIER:
				enterOuterAlt(_localctx, 1);
				{
				setState(1018);
				columnDefinition();
				}
				break;
			case LIKE:
				enterOuterAlt(_localctx, 2);
				{
				setState(1019);
				likeClause();
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
	public static class ColumnDefinitionContext extends ParserRuleContext {
		public IdentifierContext identifier() {
			return getRuleContext(IdentifierContext.class,0);
		}
		public TypeContext type() {
			return getRuleContext(TypeContext.class,0);
		}
		public TerminalNode NOT() { return getToken(SqlBaseParser.NOT, 0); }
		public TerminalNode NULL() { return getToken(SqlBaseParser.NULL, 0); }
		public TerminalNode COMMENT() { return getToken(SqlBaseParser.COMMENT, 0); }
		public StringContext string() {
			return getRuleContext(StringContext.class,0);
		}
		public TerminalNode WITH() { return getToken(SqlBaseParser.WITH, 0); }
		public PropertiesContext properties() {
			return getRuleContext(PropertiesContext.class,0);
		}
		public ColumnDefinitionContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_columnDefinition; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterColumnDefinition(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitColumnDefinition(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitColumnDefinition(this);
			else return visitor.visitChildren(this);
		}
	}

	public final ColumnDefinitionContext columnDefinition() throws RecognitionException {
		ColumnDefinitionContext _localctx = new ColumnDefinitionContext(_ctx, getState());
		enterRule(_localctx, 18, RULE_columnDefinition);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(1022);
			identifier();
			setState(1023);
			type(0);
			setState(1026);
			_errHandler.sync(this);
			_la = _input.LA(1);
			if (_la==NOT) {
				{
				setState(1024);
				match(NOT);
				setState(1025);
				match(NULL);
				}
			}

			setState(1030);
			_errHandler.sync(this);
			_la = _input.LA(1);
			if (_la==COMMENT) {
				{
				setState(1028);
				match(COMMENT);
				setState(1029);
				string();
				}
			}

			setState(1034);
			_errHandler.sync(this);
			_la = _input.LA(1);
			if (_la==WITH) {
				{
				setState(1032);
				match(WITH);
				setState(1033);
				properties();
				}
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
	public static class LikeClauseContext extends ParserRuleContext {
		public Token optionType;
		public TerminalNode LIKE() { return getToken(SqlBaseParser.LIKE, 0); }
		public QualifiedNameContext qualifiedName() {
			return getRuleContext(QualifiedNameContext.class,0);
		}
		public TerminalNode PROPERTIES() { return getToken(SqlBaseParser.PROPERTIES, 0); }
		public TerminalNode INCLUDING() { return getToken(SqlBaseParser.INCLUDING, 0); }
		public TerminalNode EXCLUDING() { return getToken(SqlBaseParser.EXCLUDING, 0); }
		public LikeClauseContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_likeClause; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterLikeClause(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitLikeClause(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitLikeClause(this);
			else return visitor.visitChildren(this);
		}
	}

	public final LikeClauseContext likeClause() throws RecognitionException {
		LikeClauseContext _localctx = new LikeClauseContext(_ctx, getState());
		enterRule(_localctx, 20, RULE_likeClause);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(1036);
			match(LIKE);
			setState(1037);
			qualifiedName();
			setState(1040);
			_errHandler.sync(this);
			_la = _input.LA(1);
			if (_la==EXCLUDING || _la==INCLUDING) {
				{
				setState(1038);
				((LikeClauseContext)_localctx).optionType = _input.LT(1);
				_la = _input.LA(1);
				if ( !(_la==EXCLUDING || _la==INCLUDING) ) {
					((LikeClauseContext)_localctx).optionType = (Token)_errHandler.recoverInline(this);
				}
				else {
					if ( _input.LA(1)==Token.EOF ) matchedEOF = true;
					_errHandler.reportMatch(this);
					consume();
				}
				setState(1039);
				match(PROPERTIES);
				}
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
	public static class PropertiesContext extends ParserRuleContext {
		public PropertyAssignmentsContext propertyAssignments() {
			return getRuleContext(PropertyAssignmentsContext.class,0);
		}
		public PropertiesContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_properties; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterProperties(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitProperties(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitProperties(this);
			else return visitor.visitChildren(this);
		}
	}

	public final PropertiesContext properties() throws RecognitionException {
		PropertiesContext _localctx = new PropertiesContext(_ctx, getState());
		enterRule(_localctx, 22, RULE_properties);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(1042);
			match(T__1);
			setState(1043);
			propertyAssignments();
			setState(1044);
			match(T__2);
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
	public static class PropertyAssignmentsContext extends ParserRuleContext {
		public List<PropertyContext> property() {
			return getRuleContexts(PropertyContext.class);
		}
		public PropertyContext property(int i) {
			return getRuleContext(PropertyContext.class,i);
		}
		public PropertyAssignmentsContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_propertyAssignments; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterPropertyAssignments(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitPropertyAssignments(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitPropertyAssignments(this);
			else return visitor.visitChildren(this);
		}
	}

	public final PropertyAssignmentsContext propertyAssignments() throws RecognitionException {
		PropertyAssignmentsContext _localctx = new PropertyAssignmentsContext(_ctx, getState());
		enterRule(_localctx, 24, RULE_propertyAssignments);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(1046);
			property();
			setState(1051);
			_errHandler.sync(this);
			_la = _input.LA(1);
			while (_la==T__3) {
				{
				{
				setState(1047);
				match(T__3);
				setState(1048);
				property();
				}
				}
				setState(1053);
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
	public static class PropertyContext extends ParserRuleContext {
		public IdentifierContext identifier() {
			return getRuleContext(IdentifierContext.class,0);
		}
		public TerminalNode EQ() { return getToken(SqlBaseParser.EQ, 0); }
		public PropertyValueContext propertyValue() {
			return getRuleContext(PropertyValueContext.class,0);
		}
		public PropertyContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_property; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterProperty(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitProperty(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitProperty(this);
			else return visitor.visitChildren(this);
		}
	}

	public final PropertyContext property() throws RecognitionException {
		PropertyContext _localctx = new PropertyContext(_ctx, getState());
		enterRule(_localctx, 26, RULE_property);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(1054);
			identifier();
			setState(1055);
			match(EQ);
			setState(1056);
			propertyValue();
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
	public static class PropertyValueContext extends ParserRuleContext {
		public PropertyValueContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_propertyValue; }
	 
		public PropertyValueContext() { }
		public void copyFrom(PropertyValueContext ctx) {
			super.copyFrom(ctx);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class DefaultPropertyValueContext extends PropertyValueContext {
		public TerminalNode DEFAULT() { return getToken(SqlBaseParser.DEFAULT, 0); }
		public DefaultPropertyValueContext(PropertyValueContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterDefaultPropertyValue(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitDefaultPropertyValue(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitDefaultPropertyValue(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class NonDefaultPropertyValueContext extends PropertyValueContext {
		public ExpressionContext expression() {
			return getRuleContext(ExpressionContext.class,0);
		}
		public NonDefaultPropertyValueContext(PropertyValueContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterNonDefaultPropertyValue(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitNonDefaultPropertyValue(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitNonDefaultPropertyValue(this);
			else return visitor.visitChildren(this);
		}
	}

	public final PropertyValueContext propertyValue() throws RecognitionException {
		PropertyValueContext _localctx = new PropertyValueContext(_ctx, getState());
		enterRule(_localctx, 28, RULE_propertyValue);
		try {
			setState(1060);
			_errHandler.sync(this);
			switch ( getInterpreter().adaptivePredict(_input,119,_ctx) ) {
			case 1:
				_localctx = new DefaultPropertyValueContext(_localctx);
				enterOuterAlt(_localctx, 1);
				{
				setState(1058);
				match(DEFAULT);
				}
				break;
			case 2:
				_localctx = new NonDefaultPropertyValueContext(_localctx);
				enterOuterAlt(_localctx, 2);
				{
				setState(1059);
				expression();
				}
				break;
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
	public static class QueryNoWithContext extends ParserRuleContext {
		public RowCountContext offset;
		public LimitRowCountContext limit;
		public RowCountContext fetchFirst;
		public QueryTermContext queryTerm() {
			return getRuleContext(QueryTermContext.class,0);
		}
		public TerminalNode ORDER() { return getToken(SqlBaseParser.ORDER, 0); }
		public TerminalNode BY() { return getToken(SqlBaseParser.BY, 0); }
		public List<SortItemContext> sortItem() {
			return getRuleContexts(SortItemContext.class);
		}
		public SortItemContext sortItem(int i) {
			return getRuleContext(SortItemContext.class,i);
		}
		public TerminalNode LIMIT() { return getToken(SqlBaseParser.LIMIT, 0); }
		public TerminalNode OFFSET() { return getToken(SqlBaseParser.OFFSET, 0); }
		public LimitRowCountContext limitRowCount() {
			return getRuleContext(LimitRowCountContext.class,0);
		}
		public List<RowCountContext> rowCount() {
			return getRuleContexts(RowCountContext.class);
		}
		public RowCountContext rowCount(int i) {
			return getRuleContext(RowCountContext.class,i);
		}
		public PgCastContext pgCast() {
			return getRuleContext(PgCastContext.class,0);
		}
		public TerminalNode FETCH() { return getToken(SqlBaseParser.FETCH, 0); }
		public List<TerminalNode> ROW() { return getTokens(SqlBaseParser.ROW); }
		public TerminalNode ROW(int i) {
			return getToken(SqlBaseParser.ROW, i);
		}
		public List<TerminalNode> ROWS() { return getTokens(SqlBaseParser.ROWS); }
		public TerminalNode ROWS(int i) {
			return getToken(SqlBaseParser.ROWS, i);
		}
		public TerminalNode FIRST() { return getToken(SqlBaseParser.FIRST, 0); }
		public TerminalNode NEXT() { return getToken(SqlBaseParser.NEXT, 0); }
		public TerminalNode ONLY() { return getToken(SqlBaseParser.ONLY, 0); }
		public TerminalNode WITH() { return getToken(SqlBaseParser.WITH, 0); }
		public TerminalNode TIES() { return getToken(SqlBaseParser.TIES, 0); }
		public QueryNoWithContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_queryNoWith; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterQueryNoWith(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitQueryNoWith(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitQueryNoWith(this);
			else return visitor.visitChildren(this);
		}
	}

	public final QueryNoWithContext queryNoWith() throws RecognitionException {
		QueryNoWithContext _localctx = new QueryNoWithContext(_ctx, getState());
		enterRule(_localctx, 30, RULE_queryNoWith);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(1062);
			queryTerm(0);
			setState(1073);
			_errHandler.sync(this);
			_la = _input.LA(1);
			if (_la==ORDER) {
				{
				setState(1063);
				match(ORDER);
				setState(1064);
				match(BY);
				setState(1065);
				sortItem();
				setState(1070);
				_errHandler.sync(this);
				_la = _input.LA(1);
				while (_la==T__3) {
					{
					{
					setState(1066);
					match(T__3);
					setState(1067);
					sortItem();
					}
					}
					setState(1072);
					_errHandler.sync(this);
					_la = _input.LA(1);
				}
				}
			}

			setState(1114);
			_errHandler.sync(this);
			switch ( getInterpreter().adaptivePredict(_input,132,_ctx) ) {
			case 1:
				{
				{
				setState(1080);
				_errHandler.sync(this);
				_la = _input.LA(1);
				if (_la==OFFSET) {
					{
					setState(1075);
					match(OFFSET);
					setState(1076);
					((QueryNoWithContext)_localctx).offset = rowCount();
					setState(1078);
					_errHandler.sync(this);
					_la = _input.LA(1);
					if (_la==ROW || _la==ROWS) {
						{
						setState(1077);
						_la = _input.LA(1);
						if ( !(_la==ROW || _la==ROWS) ) {
						_errHandler.recoverInline(this);
						}
						else {
							if ( _input.LA(1)==Token.EOF ) matchedEOF = true;
							_errHandler.reportMatch(this);
							consume();
						}
						}
					}

					}
				}

				setState(1098);
				_errHandler.sync(this);
				switch (_input.LA(1)) {
				case LIMIT:
					{
					{
					setState(1082);
					match(LIMIT);
					setState(1083);
					((QueryNoWithContext)_localctx).limit = limitRowCount();
					setState(1085);
					_errHandler.sync(this);
					_la = _input.LA(1);
					if (_la==PG_CAST) {
						{
						setState(1084);
						pgCast();
						}
					}

					}
					}
					break;
				case FETCH:
					{
					{
					setState(1087);
					match(FETCH);
					setState(1088);
					_la = _input.LA(1);
					if ( !(_la==FIRST || _la==NEXT) ) {
					_errHandler.recoverInline(this);
					}
					else {
						if ( _input.LA(1)==Token.EOF ) matchedEOF = true;
						_errHandler.reportMatch(this);
						consume();
					}
					setState(1090);
					_errHandler.sync(this);
					_la = _input.LA(1);
					if (_la==QUESTION_MARK || _la==INTEGER_VALUE) {
						{
						setState(1089);
						((QueryNoWithContext)_localctx).fetchFirst = rowCount();
						}
					}

					setState(1092);
					_la = _input.LA(1);
					if ( !(_la==ROW || _la==ROWS) ) {
					_errHandler.recoverInline(this);
					}
					else {
						if ( _input.LA(1)==Token.EOF ) matchedEOF = true;
						_errHandler.reportMatch(this);
						consume();
					}
					setState(1096);
					_errHandler.sync(this);
					switch (_input.LA(1)) {
					case ONLY:
						{
						setState(1093);
						match(ONLY);
						}
						break;
					case WITH:
						{
						setState(1094);
						match(WITH);
						setState(1095);
						match(TIES);
						}
						break;
					default:
						throw new NoViableAltException(this);
					}
					}
					}
					break;
				case EOF:
				case T__2:
				case WITH:
					break;
				default:
					break;
				}
				}
				}
				break;
			case 2:
				{
				setState(1105);
				_errHandler.sync(this);
				_la = _input.LA(1);
				if (_la==LIMIT) {
					{
					setState(1100);
					match(LIMIT);
					setState(1101);
					((QueryNoWithContext)_localctx).limit = limitRowCount();
					setState(1103);
					_errHandler.sync(this);
					_la = _input.LA(1);
					if (_la==PG_CAST) {
						{
						setState(1102);
						pgCast();
						}
					}

					}
				}

				setState(1112);
				_errHandler.sync(this);
				_la = _input.LA(1);
				if (_la==OFFSET) {
					{
					setState(1107);
					match(OFFSET);
					setState(1108);
					((QueryNoWithContext)_localctx).offset = rowCount();
					setState(1110);
					_errHandler.sync(this);
					_la = _input.LA(1);
					if (_la==ROW || _la==ROWS) {
						{
						setState(1109);
						_la = _input.LA(1);
						if ( !(_la==ROW || _la==ROWS) ) {
						_errHandler.recoverInline(this);
						}
						else {
							if ( _input.LA(1)==Token.EOF ) matchedEOF = true;
							_errHandler.reportMatch(this);
							consume();
						}
						}
					}

					}
				}

				}
				break;
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
	public static class PgCastContext extends ParserRuleContext {
		public TerminalNode PG_CAST() { return getToken(SqlBaseParser.PG_CAST, 0); }
		public IdentifierContext identifier() {
			return getRuleContext(IdentifierContext.class,0);
		}
		public TerminalNode IDENTIFIER() { return getToken(SqlBaseParser.IDENTIFIER, 0); }
		public PgCastContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_pgCast; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterPgCast(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitPgCast(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitPgCast(this);
			else return visitor.visitChildren(this);
		}
	}

	public final PgCastContext pgCast() throws RecognitionException {
		PgCastContext _localctx = new PgCastContext(_ctx, getState());
		enterRule(_localctx, 32, RULE_pgCast);
		try {
			enterOuterAlt(_localctx, 1);
			{
			{
			setState(1116);
			match(PG_CAST);
			setState(1119);
			_errHandler.sync(this);
			switch ( getInterpreter().adaptivePredict(_input,133,_ctx) ) {
			case 1:
				{
				setState(1117);
				match(IDENTIFIER);
				setState(1118);
				match(T__0);
				}
				break;
			}
			setState(1121);
			identifier();
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
	public static class LimitRowCountContext extends ParserRuleContext {
		public TerminalNode ALL() { return getToken(SqlBaseParser.ALL, 0); }
		public RowCountContext rowCount() {
			return getRuleContext(RowCountContext.class,0);
		}
		public StringContext string() {
			return getRuleContext(StringContext.class,0);
		}
		public LimitRowCountContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_limitRowCount; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterLimitRowCount(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitLimitRowCount(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitLimitRowCount(this);
			else return visitor.visitChildren(this);
		}
	}

	public final LimitRowCountContext limitRowCount() throws RecognitionException {
		LimitRowCountContext _localctx = new LimitRowCountContext(_ctx, getState());
		enterRule(_localctx, 34, RULE_limitRowCount);
		try {
			setState(1126);
			_errHandler.sync(this);
			switch (_input.LA(1)) {
			case ALL:
				enterOuterAlt(_localctx, 1);
				{
				setState(1123);
				match(ALL);
				}
				break;
			case QUESTION_MARK:
			case INTEGER_VALUE:
				enterOuterAlt(_localctx, 2);
				{
				setState(1124);
				rowCount();
				}
				break;
			case STRING:
			case UNICODE_STRING:
			case ESCAPED_STRING:
				enterOuterAlt(_localctx, 3);
				{
				setState(1125);
				string();
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
	public static class RowCountContext extends ParserRuleContext {
		public TerminalNode INTEGER_VALUE() { return getToken(SqlBaseParser.INTEGER_VALUE, 0); }
		public TerminalNode QUESTION_MARK() { return getToken(SqlBaseParser.QUESTION_MARK, 0); }
		public RowCountContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_rowCount; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterRowCount(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitRowCount(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitRowCount(this);
			else return visitor.visitChildren(this);
		}
	}

	public final RowCountContext rowCount() throws RecognitionException {
		RowCountContext _localctx = new RowCountContext(_ctx, getState());
		enterRule(_localctx, 36, RULE_rowCount);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(1128);
			_la = _input.LA(1);
			if ( !(_la==QUESTION_MARK || _la==INTEGER_VALUE) ) {
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

	@SuppressWarnings("CheckReturnValue")
	public static class QueryTermContext extends ParserRuleContext {
		public QueryTermContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_queryTerm; }
	 
		public QueryTermContext() { }
		public void copyFrom(QueryTermContext ctx) {
			super.copyFrom(ctx);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class QueryTermDefaultContext extends QueryTermContext {
		public QueryPrimaryContext queryPrimary() {
			return getRuleContext(QueryPrimaryContext.class,0);
		}
		public QueryTermDefaultContext(QueryTermContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterQueryTermDefault(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitQueryTermDefault(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitQueryTermDefault(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class SetOperationContext extends QueryTermContext {
		public QueryTermContext left;
		public Token operator;
		public QueryTermContext right;
		public List<QueryTermContext> queryTerm() {
			return getRuleContexts(QueryTermContext.class);
		}
		public QueryTermContext queryTerm(int i) {
			return getRuleContext(QueryTermContext.class,i);
		}
		public TerminalNode INTERSECT() { return getToken(SqlBaseParser.INTERSECT, 0); }
		public SetQuantifierContext setQuantifier() {
			return getRuleContext(SetQuantifierContext.class,0);
		}
		public TerminalNode UNION() { return getToken(SqlBaseParser.UNION, 0); }
		public TerminalNode EXCEPT() { return getToken(SqlBaseParser.EXCEPT, 0); }
		public SetOperationContext(QueryTermContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterSetOperation(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitSetOperation(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitSetOperation(this);
			else return visitor.visitChildren(this);
		}
	}

	public final QueryTermContext queryTerm() throws RecognitionException {
		return queryTerm(0);
	}

	private QueryTermContext queryTerm(int _p) throws RecognitionException {
		ParserRuleContext _parentctx = _ctx;
		int _parentState = getState();
		QueryTermContext _localctx = new QueryTermContext(_ctx, _parentState);
		QueryTermContext _prevctx = _localctx;
		int _startState = 38;
		enterRecursionRule(_localctx, 38, RULE_queryTerm, _p);
		int _la;
		try {
			int _alt;
			enterOuterAlt(_localctx, 1);
			{
			{
			_localctx = new QueryTermDefaultContext(_localctx);
			_ctx = _localctx;
			_prevctx = _localctx;

			setState(1131);
			queryPrimary();
			}
			_ctx.stop = _input.LT(-1);
			setState(1147);
			_errHandler.sync(this);
			_alt = getInterpreter().adaptivePredict(_input,138,_ctx);
			while ( _alt!=2 && _alt!=org.antlr.v4.runtime.atn.ATN.INVALID_ALT_NUMBER ) {
				if ( _alt==1 ) {
					if ( _parseListeners!=null ) triggerExitRuleEvent();
					_prevctx = _localctx;
					{
					setState(1145);
					_errHandler.sync(this);
					switch ( getInterpreter().adaptivePredict(_input,137,_ctx) ) {
					case 1:
						{
						_localctx = new SetOperationContext(new QueryTermContext(_parentctx, _parentState));
						((SetOperationContext)_localctx).left = _prevctx;
						pushNewRecursionContext(_localctx, _startState, RULE_queryTerm);
						setState(1133);
						if (!(precpred(_ctx, 2))) throw new FailedPredicateException(this, "precpred(_ctx, 2)");
						setState(1134);
						((SetOperationContext)_localctx).operator = match(INTERSECT);
						setState(1136);
						_errHandler.sync(this);
						_la = _input.LA(1);
						if (_la==ALL || _la==DISTINCT) {
							{
							setState(1135);
							setQuantifier();
							}
						}

						setState(1138);
						((SetOperationContext)_localctx).right = queryTerm(3);
						}
						break;
					case 2:
						{
						_localctx = new SetOperationContext(new QueryTermContext(_parentctx, _parentState));
						((SetOperationContext)_localctx).left = _prevctx;
						pushNewRecursionContext(_localctx, _startState, RULE_queryTerm);
						setState(1139);
						if (!(precpred(_ctx, 1))) throw new FailedPredicateException(this, "precpred(_ctx, 1)");
						setState(1140);
						((SetOperationContext)_localctx).operator = _input.LT(1);
						_la = _input.LA(1);
						if ( !(_la==EXCEPT || _la==UNION) ) {
							((SetOperationContext)_localctx).operator = (Token)_errHandler.recoverInline(this);
						}
						else {
							if ( _input.LA(1)==Token.EOF ) matchedEOF = true;
							_errHandler.reportMatch(this);
							consume();
						}
						setState(1142);
						_errHandler.sync(this);
						_la = _input.LA(1);
						if (_la==ALL || _la==DISTINCT) {
							{
							setState(1141);
							setQuantifier();
							}
						}

						setState(1144);
						((SetOperationContext)_localctx).right = queryTerm(2);
						}
						break;
					}
					} 
				}
				setState(1149);
				_errHandler.sync(this);
				_alt = getInterpreter().adaptivePredict(_input,138,_ctx);
			}
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			unrollRecursionContexts(_parentctx);
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class QueryPrimaryContext extends ParserRuleContext {
		public QueryPrimaryContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_queryPrimary; }
	 
		public QueryPrimaryContext() { }
		public void copyFrom(QueryPrimaryContext ctx) {
			super.copyFrom(ctx);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class SubqueryContext extends QueryPrimaryContext {
		public QueryNoWithContext queryNoWith() {
			return getRuleContext(QueryNoWithContext.class,0);
		}
		public SubqueryContext(QueryPrimaryContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterSubquery(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitSubquery(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitSubquery(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class QueryPrimaryDefaultContext extends QueryPrimaryContext {
		public QuerySpecificationContext querySpecification() {
			return getRuleContext(QuerySpecificationContext.class,0);
		}
		public QueryPrimaryDefaultContext(QueryPrimaryContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterQueryPrimaryDefault(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitQueryPrimaryDefault(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitQueryPrimaryDefault(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class TableContext extends QueryPrimaryContext {
		public TerminalNode TABLE() { return getToken(SqlBaseParser.TABLE, 0); }
		public QualifiedNameContext qualifiedName() {
			return getRuleContext(QualifiedNameContext.class,0);
		}
		public TableContext(QueryPrimaryContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterTable(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitTable(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitTable(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class InlineTableContext extends QueryPrimaryContext {
		public TerminalNode VALUES() { return getToken(SqlBaseParser.VALUES, 0); }
		public List<ExpressionContext> expression() {
			return getRuleContexts(ExpressionContext.class);
		}
		public ExpressionContext expression(int i) {
			return getRuleContext(ExpressionContext.class,i);
		}
		public InlineTableContext(QueryPrimaryContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterInlineTable(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitInlineTable(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitInlineTable(this);
			else return visitor.visitChildren(this);
		}
	}

	public final QueryPrimaryContext queryPrimary() throws RecognitionException {
		QueryPrimaryContext _localctx = new QueryPrimaryContext(_ctx, getState());
		enterRule(_localctx, 40, RULE_queryPrimary);
		try {
			int _alt;
			setState(1166);
			_errHandler.sync(this);
			switch (_input.LA(1)) {
			case SELECT:
				_localctx = new QueryPrimaryDefaultContext(_localctx);
				enterOuterAlt(_localctx, 1);
				{
				setState(1150);
				querySpecification();
				}
				break;
			case TABLE:
				_localctx = new TableContext(_localctx);
				enterOuterAlt(_localctx, 2);
				{
				setState(1151);
				match(TABLE);
				setState(1152);
				qualifiedName();
				}
				break;
			case VALUES:
				_localctx = new InlineTableContext(_localctx);
				enterOuterAlt(_localctx, 3);
				{
				setState(1153);
				match(VALUES);
				setState(1154);
				expression();
				setState(1159);
				_errHandler.sync(this);
				_alt = getInterpreter().adaptivePredict(_input,139,_ctx);
				while ( _alt!=2 && _alt!=org.antlr.v4.runtime.atn.ATN.INVALID_ALT_NUMBER ) {
					if ( _alt==1 ) {
						{
						{
						setState(1155);
						match(T__3);
						setState(1156);
						expression();
						}
						} 
					}
					setState(1161);
					_errHandler.sync(this);
					_alt = getInterpreter().adaptivePredict(_input,139,_ctx);
				}
				}
				break;
			case T__1:
				_localctx = new SubqueryContext(_localctx);
				enterOuterAlt(_localctx, 4);
				{
				setState(1162);
				match(T__1);
				setState(1163);
				queryNoWith();
				setState(1164);
				match(T__2);
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
	public static class SortItemContext extends ParserRuleContext {
		public Token ordering;
		public Token nullOrdering;
		public ExpressionContext expression() {
			return getRuleContext(ExpressionContext.class,0);
		}
		public TerminalNode NULLS() { return getToken(SqlBaseParser.NULLS, 0); }
		public TerminalNode ASC() { return getToken(SqlBaseParser.ASC, 0); }
		public TerminalNode DESC() { return getToken(SqlBaseParser.DESC, 0); }
		public TerminalNode FIRST() { return getToken(SqlBaseParser.FIRST, 0); }
		public TerminalNode LAST() { return getToken(SqlBaseParser.LAST, 0); }
		public SortItemContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_sortItem; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterSortItem(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitSortItem(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitSortItem(this);
			else return visitor.visitChildren(this);
		}
	}

	public final SortItemContext sortItem() throws RecognitionException {
		SortItemContext _localctx = new SortItemContext(_ctx, getState());
		enterRule(_localctx, 42, RULE_sortItem);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(1168);
			expression();
			setState(1170);
			_errHandler.sync(this);
			_la = _input.LA(1);
			if (_la==ASC || _la==DESC) {
				{
				setState(1169);
				((SortItemContext)_localctx).ordering = _input.LT(1);
				_la = _input.LA(1);
				if ( !(_la==ASC || _la==DESC) ) {
					((SortItemContext)_localctx).ordering = (Token)_errHandler.recoverInline(this);
				}
				else {
					if ( _input.LA(1)==Token.EOF ) matchedEOF = true;
					_errHandler.reportMatch(this);
					consume();
				}
				}
			}

			setState(1174);
			_errHandler.sync(this);
			_la = _input.LA(1);
			if (_la==NULLS) {
				{
				setState(1172);
				match(NULLS);
				setState(1173);
				((SortItemContext)_localctx).nullOrdering = _input.LT(1);
				_la = _input.LA(1);
				if ( !(_la==FIRST || _la==LAST) ) {
					((SortItemContext)_localctx).nullOrdering = (Token)_errHandler.recoverInline(this);
				}
				else {
					if ( _input.LA(1)==Token.EOF ) matchedEOF = true;
					_errHandler.reportMatch(this);
					consume();
				}
				}
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
	public static class QuerySpecificationContext extends ParserRuleContext {
		public BooleanExpressionContext where;
		public BooleanExpressionContext having;
		public TerminalNode SELECT() { return getToken(SqlBaseParser.SELECT, 0); }
		public List<SelectItemContext> selectItem() {
			return getRuleContexts(SelectItemContext.class);
		}
		public SelectItemContext selectItem(int i) {
			return getRuleContext(SelectItemContext.class,i);
		}
		public SetQuantifierContext setQuantifier() {
			return getRuleContext(SetQuantifierContext.class,0);
		}
		public TerminalNode FROM() { return getToken(SqlBaseParser.FROM, 0); }
		public List<RelationContext> relation() {
			return getRuleContexts(RelationContext.class);
		}
		public RelationContext relation(int i) {
			return getRuleContext(RelationContext.class,i);
		}
		public TerminalNode WHERE() { return getToken(SqlBaseParser.WHERE, 0); }
		public TerminalNode GROUP() { return getToken(SqlBaseParser.GROUP, 0); }
		public TerminalNode BY() { return getToken(SqlBaseParser.BY, 0); }
		public GroupByContext groupBy() {
			return getRuleContext(GroupByContext.class,0);
		}
		public TerminalNode HAVING() { return getToken(SqlBaseParser.HAVING, 0); }
		public TerminalNode WINDOW() { return getToken(SqlBaseParser.WINDOW, 0); }
		public List<WindowDefinitionContext> windowDefinition() {
			return getRuleContexts(WindowDefinitionContext.class);
		}
		public WindowDefinitionContext windowDefinition(int i) {
			return getRuleContext(WindowDefinitionContext.class,i);
		}
		public List<BooleanExpressionContext> booleanExpression() {
			return getRuleContexts(BooleanExpressionContext.class);
		}
		public BooleanExpressionContext booleanExpression(int i) {
			return getRuleContext(BooleanExpressionContext.class,i);
		}
		public QuerySpecificationContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_querySpecification; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterQuerySpecification(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitQuerySpecification(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitQuerySpecification(this);
			else return visitor.visitChildren(this);
		}
	}

	public final QuerySpecificationContext querySpecification() throws RecognitionException {
		QuerySpecificationContext _localctx = new QuerySpecificationContext(_ctx, getState());
		enterRule(_localctx, 44, RULE_querySpecification);
		try {
			int _alt;
			enterOuterAlt(_localctx, 1);
			{
			setState(1176);
			match(SELECT);
			setState(1178);
			_errHandler.sync(this);
			switch ( getInterpreter().adaptivePredict(_input,143,_ctx) ) {
			case 1:
				{
				setState(1177);
				setQuantifier();
				}
				break;
			}
			setState(1180);
			selectItem();
			setState(1185);
			_errHandler.sync(this);
			_alt = getInterpreter().adaptivePredict(_input,144,_ctx);
			while ( _alt!=2 && _alt!=org.antlr.v4.runtime.atn.ATN.INVALID_ALT_NUMBER ) {
				if ( _alt==1 ) {
					{
					{
					setState(1181);
					match(T__3);
					setState(1182);
					selectItem();
					}
					} 
				}
				setState(1187);
				_errHandler.sync(this);
				_alt = getInterpreter().adaptivePredict(_input,144,_ctx);
			}
			setState(1197);
			_errHandler.sync(this);
			switch ( getInterpreter().adaptivePredict(_input,146,_ctx) ) {
			case 1:
				{
				setState(1188);
				match(FROM);
				setState(1189);
				relation(0);
				setState(1194);
				_errHandler.sync(this);
				_alt = getInterpreter().adaptivePredict(_input,145,_ctx);
				while ( _alt!=2 && _alt!=org.antlr.v4.runtime.atn.ATN.INVALID_ALT_NUMBER ) {
					if ( _alt==1 ) {
						{
						{
						setState(1190);
						match(T__3);
						setState(1191);
						relation(0);
						}
						} 
					}
					setState(1196);
					_errHandler.sync(this);
					_alt = getInterpreter().adaptivePredict(_input,145,_ctx);
				}
				}
				break;
			}
			setState(1201);
			_errHandler.sync(this);
			switch ( getInterpreter().adaptivePredict(_input,147,_ctx) ) {
			case 1:
				{
				setState(1199);
				match(WHERE);
				setState(1200);
				((QuerySpecificationContext)_localctx).where = booleanExpression(0);
				}
				break;
			}
			setState(1206);
			_errHandler.sync(this);
			switch ( getInterpreter().adaptivePredict(_input,148,_ctx) ) {
			case 1:
				{
				setState(1203);
				match(GROUP);
				setState(1204);
				match(BY);
				setState(1205);
				groupBy();
				}
				break;
			}
			setState(1210);
			_errHandler.sync(this);
			switch ( getInterpreter().adaptivePredict(_input,149,_ctx) ) {
			case 1:
				{
				setState(1208);
				match(HAVING);
				setState(1209);
				((QuerySpecificationContext)_localctx).having = booleanExpression(0);
				}
				break;
			}
			setState(1221);
			_errHandler.sync(this);
			switch ( getInterpreter().adaptivePredict(_input,151,_ctx) ) {
			case 1:
				{
				setState(1212);
				match(WINDOW);
				setState(1213);
				windowDefinition();
				setState(1218);
				_errHandler.sync(this);
				_alt = getInterpreter().adaptivePredict(_input,150,_ctx);
				while ( _alt!=2 && _alt!=org.antlr.v4.runtime.atn.ATN.INVALID_ALT_NUMBER ) {
					if ( _alt==1 ) {
						{
						{
						setState(1214);
						match(T__3);
						setState(1215);
						windowDefinition();
						}
						} 
					}
					setState(1220);
					_errHandler.sync(this);
					_alt = getInterpreter().adaptivePredict(_input,150,_ctx);
				}
				}
				break;
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
	public static class GroupByContext extends ParserRuleContext {
		public List<GroupingElementContext> groupingElement() {
			return getRuleContexts(GroupingElementContext.class);
		}
		public GroupingElementContext groupingElement(int i) {
			return getRuleContext(GroupingElementContext.class,i);
		}
		public SetQuantifierContext setQuantifier() {
			return getRuleContext(SetQuantifierContext.class,0);
		}
		public GroupByContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_groupBy; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterGroupBy(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitGroupBy(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitGroupBy(this);
			else return visitor.visitChildren(this);
		}
	}

	public final GroupByContext groupBy() throws RecognitionException {
		GroupByContext _localctx = new GroupByContext(_ctx, getState());
		enterRule(_localctx, 46, RULE_groupBy);
		try {
			int _alt;
			enterOuterAlt(_localctx, 1);
			{
			setState(1224);
			_errHandler.sync(this);
			switch ( getInterpreter().adaptivePredict(_input,152,_ctx) ) {
			case 1:
				{
				setState(1223);
				setQuantifier();
				}
				break;
			}
			setState(1226);
			groupingElement();
			setState(1231);
			_errHandler.sync(this);
			_alt = getInterpreter().adaptivePredict(_input,153,_ctx);
			while ( _alt!=2 && _alt!=org.antlr.v4.runtime.atn.ATN.INVALID_ALT_NUMBER ) {
				if ( _alt==1 ) {
					{
					{
					setState(1227);
					match(T__3);
					setState(1228);
					groupingElement();
					}
					} 
				}
				setState(1233);
				_errHandler.sync(this);
				_alt = getInterpreter().adaptivePredict(_input,153,_ctx);
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
	public static class GroupingElementContext extends ParserRuleContext {
		public GroupingElementContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_groupingElement; }
	 
		public GroupingElementContext() { }
		public void copyFrom(GroupingElementContext ctx) {
			super.copyFrom(ctx);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class MultipleGroupingSetsContext extends GroupingElementContext {
		public TerminalNode GROUPING() { return getToken(SqlBaseParser.GROUPING, 0); }
		public TerminalNode SETS() { return getToken(SqlBaseParser.SETS, 0); }
		public List<GroupingSetContext> groupingSet() {
			return getRuleContexts(GroupingSetContext.class);
		}
		public GroupingSetContext groupingSet(int i) {
			return getRuleContext(GroupingSetContext.class,i);
		}
		public MultipleGroupingSetsContext(GroupingElementContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterMultipleGroupingSets(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitMultipleGroupingSets(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitMultipleGroupingSets(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class SingleGroupingSetContext extends GroupingElementContext {
		public GroupingSetContext groupingSet() {
			return getRuleContext(GroupingSetContext.class,0);
		}
		public SingleGroupingSetContext(GroupingElementContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterSingleGroupingSet(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitSingleGroupingSet(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitSingleGroupingSet(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class CubeContext extends GroupingElementContext {
		public TerminalNode CUBE() { return getToken(SqlBaseParser.CUBE, 0); }
		public List<ExpressionContext> expression() {
			return getRuleContexts(ExpressionContext.class);
		}
		public ExpressionContext expression(int i) {
			return getRuleContext(ExpressionContext.class,i);
		}
		public CubeContext(GroupingElementContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterCube(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitCube(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitCube(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class RollupContext extends GroupingElementContext {
		public TerminalNode ROLLUP() { return getToken(SqlBaseParser.ROLLUP, 0); }
		public List<ExpressionContext> expression() {
			return getRuleContexts(ExpressionContext.class);
		}
		public ExpressionContext expression(int i) {
			return getRuleContext(ExpressionContext.class,i);
		}
		public RollupContext(GroupingElementContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterRollup(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitRollup(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitRollup(this);
			else return visitor.visitChildren(this);
		}
	}

	public final GroupingElementContext groupingElement() throws RecognitionException {
		GroupingElementContext _localctx = new GroupingElementContext(_ctx, getState());
		enterRule(_localctx, 48, RULE_groupingElement);
		int _la;
		try {
			setState(1274);
			_errHandler.sync(this);
			switch ( getInterpreter().adaptivePredict(_input,159,_ctx) ) {
			case 1:
				_localctx = new SingleGroupingSetContext(_localctx);
				enterOuterAlt(_localctx, 1);
				{
				setState(1234);
				groupingSet();
				}
				break;
			case 2:
				_localctx = new RollupContext(_localctx);
				enterOuterAlt(_localctx, 2);
				{
				setState(1235);
				match(ROLLUP);
				setState(1236);
				match(T__1);
				setState(1245);
				_errHandler.sync(this);
				_la = _input.LA(1);
				if ((((_la) & ~0x3f) == 0 && ((1L << _la) & -304556133446578172L) != 0) || ((((_la - 64)) & ~0x3f) == 0 && ((1L << (_la - 64)) & -5424665139366696073L) != 0) || ((((_la - 129)) & ~0x3f) == 0 && ((1L << (_la - 129)) & -1153018536512192553L) != 0) || ((((_la - 193)) & ~0x3f) == 0 && ((1L << (_la - 193)) & -2928466825937175555L) != 0) || ((((_la - 257)) & ~0x3f) == 0 && ((1L << (_la - 257)) & 1133846595561L) != 0)) {
					{
					setState(1237);
					expression();
					setState(1242);
					_errHandler.sync(this);
					_la = _input.LA(1);
					while (_la==T__3) {
						{
						{
						setState(1238);
						match(T__3);
						setState(1239);
						expression();
						}
						}
						setState(1244);
						_errHandler.sync(this);
						_la = _input.LA(1);
					}
					}
				}

				setState(1247);
				match(T__2);
				}
				break;
			case 3:
				_localctx = new CubeContext(_localctx);
				enterOuterAlt(_localctx, 3);
				{
				setState(1248);
				match(CUBE);
				setState(1249);
				match(T__1);
				setState(1258);
				_errHandler.sync(this);
				_la = _input.LA(1);
				if ((((_la) & ~0x3f) == 0 && ((1L << _la) & -304556133446578172L) != 0) || ((((_la - 64)) & ~0x3f) == 0 && ((1L << (_la - 64)) & -5424665139366696073L) != 0) || ((((_la - 129)) & ~0x3f) == 0 && ((1L << (_la - 129)) & -1153018536512192553L) != 0) || ((((_la - 193)) & ~0x3f) == 0 && ((1L << (_la - 193)) & -2928466825937175555L) != 0) || ((((_la - 257)) & ~0x3f) == 0 && ((1L << (_la - 257)) & 1133846595561L) != 0)) {
					{
					setState(1250);
					expression();
					setState(1255);
					_errHandler.sync(this);
					_la = _input.LA(1);
					while (_la==T__3) {
						{
						{
						setState(1251);
						match(T__3);
						setState(1252);
						expression();
						}
						}
						setState(1257);
						_errHandler.sync(this);
						_la = _input.LA(1);
					}
					}
				}

				setState(1260);
				match(T__2);
				}
				break;
			case 4:
				_localctx = new MultipleGroupingSetsContext(_localctx);
				enterOuterAlt(_localctx, 4);
				{
				setState(1261);
				match(GROUPING);
				setState(1262);
				match(SETS);
				setState(1263);
				match(T__1);
				setState(1264);
				groupingSet();
				setState(1269);
				_errHandler.sync(this);
				_la = _input.LA(1);
				while (_la==T__3) {
					{
					{
					setState(1265);
					match(T__3);
					setState(1266);
					groupingSet();
					}
					}
					setState(1271);
					_errHandler.sync(this);
					_la = _input.LA(1);
				}
				setState(1272);
				match(T__2);
				}
				break;
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
	public static class GroupingSetContext extends ParserRuleContext {
		public List<ExpressionContext> expression() {
			return getRuleContexts(ExpressionContext.class);
		}
		public ExpressionContext expression(int i) {
			return getRuleContext(ExpressionContext.class,i);
		}
		public GroupingSetContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_groupingSet; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterGroupingSet(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitGroupingSet(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitGroupingSet(this);
			else return visitor.visitChildren(this);
		}
	}

	public final GroupingSetContext groupingSet() throws RecognitionException {
		GroupingSetContext _localctx = new GroupingSetContext(_ctx, getState());
		enterRule(_localctx, 50, RULE_groupingSet);
		int _la;
		try {
			setState(1289);
			_errHandler.sync(this);
			switch ( getInterpreter().adaptivePredict(_input,162,_ctx) ) {
			case 1:
				enterOuterAlt(_localctx, 1);
				{
				setState(1276);
				match(T__1);
				setState(1285);
				_errHandler.sync(this);
				_la = _input.LA(1);
				if ((((_la) & ~0x3f) == 0 && ((1L << _la) & -304556133446578172L) != 0) || ((((_la - 64)) & ~0x3f) == 0 && ((1L << (_la - 64)) & -5424665139366696073L) != 0) || ((((_la - 129)) & ~0x3f) == 0 && ((1L << (_la - 129)) & -1153018536512192553L) != 0) || ((((_la - 193)) & ~0x3f) == 0 && ((1L << (_la - 193)) & -2928466825937175555L) != 0) || ((((_la - 257)) & ~0x3f) == 0 && ((1L << (_la - 257)) & 1133846595561L) != 0)) {
					{
					setState(1277);
					expression();
					setState(1282);
					_errHandler.sync(this);
					_la = _input.LA(1);
					while (_la==T__3) {
						{
						{
						setState(1278);
						match(T__3);
						setState(1279);
						expression();
						}
						}
						setState(1284);
						_errHandler.sync(this);
						_la = _input.LA(1);
					}
					}
				}

				setState(1287);
				match(T__2);
				}
				break;
			case 2:
				enterOuterAlt(_localctx, 2);
				{
				setState(1288);
				expression();
				}
				break;
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
	public static class WindowDefinitionContext extends ParserRuleContext {
		public IdentifierContext name;
		public TerminalNode AS() { return getToken(SqlBaseParser.AS, 0); }
		public WindowSpecificationContext windowSpecification() {
			return getRuleContext(WindowSpecificationContext.class,0);
		}
		public IdentifierContext identifier() {
			return getRuleContext(IdentifierContext.class,0);
		}
		public WindowDefinitionContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_windowDefinition; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterWindowDefinition(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitWindowDefinition(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitWindowDefinition(this);
			else return visitor.visitChildren(this);
		}
	}

	public final WindowDefinitionContext windowDefinition() throws RecognitionException {
		WindowDefinitionContext _localctx = new WindowDefinitionContext(_ctx, getState());
		enterRule(_localctx, 52, RULE_windowDefinition);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(1291);
			((WindowDefinitionContext)_localctx).name = identifier();
			setState(1292);
			match(AS);
			setState(1293);
			match(T__1);
			setState(1294);
			windowSpecification();
			setState(1295);
			match(T__2);
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
	public static class WindowSpecificationContext extends ParserRuleContext {
		public IdentifierContext existingWindowName;
		public ExpressionContext expression;
		public List<ExpressionContext> partition = new ArrayList<ExpressionContext>();
		public TerminalNode PARTITION() { return getToken(SqlBaseParser.PARTITION, 0); }
		public List<TerminalNode> BY() { return getTokens(SqlBaseParser.BY); }
		public TerminalNode BY(int i) {
			return getToken(SqlBaseParser.BY, i);
		}
		public TerminalNode ORDER() { return getToken(SqlBaseParser.ORDER, 0); }
		public List<SortItemContext> sortItem() {
			return getRuleContexts(SortItemContext.class);
		}
		public SortItemContext sortItem(int i) {
			return getRuleContext(SortItemContext.class,i);
		}
		public WindowFrameContext windowFrame() {
			return getRuleContext(WindowFrameContext.class,0);
		}
		public IdentifierContext identifier() {
			return getRuleContext(IdentifierContext.class,0);
		}
		public List<ExpressionContext> expression() {
			return getRuleContexts(ExpressionContext.class);
		}
		public ExpressionContext expression(int i) {
			return getRuleContext(ExpressionContext.class,i);
		}
		public WindowSpecificationContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_windowSpecification; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterWindowSpecification(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitWindowSpecification(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitWindowSpecification(this);
			else return visitor.visitChildren(this);
		}
	}

	public final WindowSpecificationContext windowSpecification() throws RecognitionException {
		WindowSpecificationContext _localctx = new WindowSpecificationContext(_ctx, getState());
		enterRule(_localctx, 54, RULE_windowSpecification);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(1298);
			_errHandler.sync(this);
			switch ( getInterpreter().adaptivePredict(_input,163,_ctx) ) {
			case 1:
				{
				setState(1297);
				((WindowSpecificationContext)_localctx).existingWindowName = identifier();
				}
				break;
			}
			setState(1310);
			_errHandler.sync(this);
			_la = _input.LA(1);
			if (_la==PARTITION) {
				{
				setState(1300);
				match(PARTITION);
				setState(1301);
				match(BY);
				setState(1302);
				((WindowSpecificationContext)_localctx).expression = expression();
				((WindowSpecificationContext)_localctx).partition.add(((WindowSpecificationContext)_localctx).expression);
				setState(1307);
				_errHandler.sync(this);
				_la = _input.LA(1);
				while (_la==T__3) {
					{
					{
					setState(1303);
					match(T__3);
					setState(1304);
					((WindowSpecificationContext)_localctx).expression = expression();
					((WindowSpecificationContext)_localctx).partition.add(((WindowSpecificationContext)_localctx).expression);
					}
					}
					setState(1309);
					_errHandler.sync(this);
					_la = _input.LA(1);
				}
				}
			}

			setState(1322);
			_errHandler.sync(this);
			_la = _input.LA(1);
			if (_la==ORDER) {
				{
				setState(1312);
				match(ORDER);
				setState(1313);
				match(BY);
				setState(1314);
				sortItem();
				setState(1319);
				_errHandler.sync(this);
				_la = _input.LA(1);
				while (_la==T__3) {
					{
					{
					setState(1315);
					match(T__3);
					setState(1316);
					sortItem();
					}
					}
					setState(1321);
					_errHandler.sync(this);
					_la = _input.LA(1);
				}
				}
			}

			setState(1325);
			_errHandler.sync(this);
			_la = _input.LA(1);
			if (_la==GROUPS || _la==MEASURES || _la==RANGE || _la==ROWS) {
				{
				setState(1324);
				windowFrame();
				}
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
	public static class NamedQueryContext extends ParserRuleContext {
		public IdentifierContext name;
		public TerminalNode AS() { return getToken(SqlBaseParser.AS, 0); }
		public QueryContext query() {
			return getRuleContext(QueryContext.class,0);
		}
		public IdentifierContext identifier() {
			return getRuleContext(IdentifierContext.class,0);
		}
		public ColumnAliasesContext columnAliases() {
			return getRuleContext(ColumnAliasesContext.class,0);
		}
		public NamedQueryContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_namedQuery; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterNamedQuery(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitNamedQuery(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitNamedQuery(this);
			else return visitor.visitChildren(this);
		}
	}

	public final NamedQueryContext namedQuery() throws RecognitionException {
		NamedQueryContext _localctx = new NamedQueryContext(_ctx, getState());
		enterRule(_localctx, 56, RULE_namedQuery);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(1327);
			((NamedQueryContext)_localctx).name = identifier();
			setState(1329);
			_errHandler.sync(this);
			_la = _input.LA(1);
			if (_la==T__1) {
				{
				setState(1328);
				columnAliases();
				}
			}

			setState(1331);
			match(AS);
			setState(1332);
			match(T__1);
			setState(1333);
			query();
			setState(1334);
			match(T__2);
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
	public static class SetQuantifierContext extends ParserRuleContext {
		public TerminalNode DISTINCT() { return getToken(SqlBaseParser.DISTINCT, 0); }
		public TerminalNode ALL() { return getToken(SqlBaseParser.ALL, 0); }
		public SetQuantifierContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_setQuantifier; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterSetQuantifier(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitSetQuantifier(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitSetQuantifier(this);
			else return visitor.visitChildren(this);
		}
	}

	public final SetQuantifierContext setQuantifier() throws RecognitionException {
		SetQuantifierContext _localctx = new SetQuantifierContext(_ctx, getState());
		enterRule(_localctx, 58, RULE_setQuantifier);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(1336);
			_la = _input.LA(1);
			if ( !(_la==ALL || _la==DISTINCT) ) {
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

	@SuppressWarnings("CheckReturnValue")
	public static class SelectItemContext extends ParserRuleContext {
		public SelectItemContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_selectItem; }
	 
		public SelectItemContext() { }
		public void copyFrom(SelectItemContext ctx) {
			super.copyFrom(ctx);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class SelectAllContext extends SelectItemContext {
		public PrimaryExpressionContext primaryExpression() {
			return getRuleContext(PrimaryExpressionContext.class,0);
		}
		public TerminalNode ASTERISK() { return getToken(SqlBaseParser.ASTERISK, 0); }
		public TerminalNode AS() { return getToken(SqlBaseParser.AS, 0); }
		public ColumnAliasesContext columnAliases() {
			return getRuleContext(ColumnAliasesContext.class,0);
		}
		public SelectAllContext(SelectItemContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterSelectAll(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitSelectAll(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitSelectAll(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class SelectSingleContext extends SelectItemContext {
		public ExpressionContext expression() {
			return getRuleContext(ExpressionContext.class,0);
		}
		public IdentifierContext identifier() {
			return getRuleContext(IdentifierContext.class,0);
		}
		public TerminalNode AS() { return getToken(SqlBaseParser.AS, 0); }
		public SelectSingleContext(SelectItemContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterSelectSingle(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitSelectSingle(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitSelectSingle(this);
			else return visitor.visitChildren(this);
		}
	}

	public final SelectItemContext selectItem() throws RecognitionException {
		SelectItemContext _localctx = new SelectItemContext(_ctx, getState());
		enterRule(_localctx, 60, RULE_selectItem);
		int _la;
		try {
			setState(1353);
			_errHandler.sync(this);
			switch ( getInterpreter().adaptivePredict(_input,173,_ctx) ) {
			case 1:
				_localctx = new SelectSingleContext(_localctx);
				enterOuterAlt(_localctx, 1);
				{
				setState(1338);
				expression();
				setState(1343);
				_errHandler.sync(this);
				switch ( getInterpreter().adaptivePredict(_input,171,_ctx) ) {
				case 1:
					{
					setState(1340);
					_errHandler.sync(this);
					_la = _input.LA(1);
					if (_la==AS) {
						{
						setState(1339);
						match(AS);
						}
					}

					setState(1342);
					identifier();
					}
					break;
				}
				}
				break;
			case 2:
				_localctx = new SelectAllContext(_localctx);
				enterOuterAlt(_localctx, 2);
				{
				setState(1345);
				primaryExpression(0);
				setState(1346);
				match(T__0);
				setState(1347);
				match(ASTERISK);
				setState(1350);
				_errHandler.sync(this);
				switch ( getInterpreter().adaptivePredict(_input,172,_ctx) ) {
				case 1:
					{
					setState(1348);
					match(AS);
					setState(1349);
					columnAliases();
					}
					break;
				}
				}
				break;
			case 3:
				_localctx = new SelectAllContext(_localctx);
				enterOuterAlt(_localctx, 3);
				{
				setState(1352);
				match(ASTERISK);
				}
				break;
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
	public static class RelationContext extends ParserRuleContext {
		public RelationContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_relation; }
	 
		public RelationContext() { }
		public void copyFrom(RelationContext ctx) {
			super.copyFrom(ctx);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class RelationDefaultContext extends RelationContext {
		public SampledRelationContext sampledRelation() {
			return getRuleContext(SampledRelationContext.class,0);
		}
		public RelationDefaultContext(RelationContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterRelationDefault(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitRelationDefault(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitRelationDefault(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class JoinRelationContext extends RelationContext {
		public RelationContext left;
		public SampledRelationContext right;
		public RelationContext rightRelation;
		public List<RelationContext> relation() {
			return getRuleContexts(RelationContext.class);
		}
		public RelationContext relation(int i) {
			return getRuleContext(RelationContext.class,i);
		}
		public TerminalNode CROSS() { return getToken(SqlBaseParser.CROSS, 0); }
		public TerminalNode JOIN() { return getToken(SqlBaseParser.JOIN, 0); }
		public JoinTypeContext joinType() {
			return getRuleContext(JoinTypeContext.class,0);
		}
		public JoinCriteriaContext joinCriteria() {
			return getRuleContext(JoinCriteriaContext.class,0);
		}
		public TerminalNode NATURAL() { return getToken(SqlBaseParser.NATURAL, 0); }
		public SampledRelationContext sampledRelation() {
			return getRuleContext(SampledRelationContext.class,0);
		}
		public JoinRelationContext(RelationContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterJoinRelation(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitJoinRelation(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitJoinRelation(this);
			else return visitor.visitChildren(this);
		}
	}

	public final RelationContext relation() throws RecognitionException {
		return relation(0);
	}

	private RelationContext relation(int _p) throws RecognitionException {
		ParserRuleContext _parentctx = _ctx;
		int _parentState = getState();
		RelationContext _localctx = new RelationContext(_ctx, _parentState);
		RelationContext _prevctx = _localctx;
		int _startState = 62;
		enterRecursionRule(_localctx, 62, RULE_relation, _p);
		try {
			int _alt;
			enterOuterAlt(_localctx, 1);
			{
			{
			_localctx = new RelationDefaultContext(_localctx);
			_ctx = _localctx;
			_prevctx = _localctx;

			setState(1356);
			sampledRelation();
			}
			_ctx.stop = _input.LT(-1);
			setState(1376);
			_errHandler.sync(this);
			_alt = getInterpreter().adaptivePredict(_input,175,_ctx);
			while ( _alt!=2 && _alt!=org.antlr.v4.runtime.atn.ATN.INVALID_ALT_NUMBER ) {
				if ( _alt==1 ) {
					if ( _parseListeners!=null ) triggerExitRuleEvent();
					_prevctx = _localctx;
					{
					{
					_localctx = new JoinRelationContext(new RelationContext(_parentctx, _parentState));
					((JoinRelationContext)_localctx).left = _prevctx;
					pushNewRecursionContext(_localctx, _startState, RULE_relation);
					setState(1358);
					if (!(precpred(_ctx, 2))) throw new FailedPredicateException(this, "precpred(_ctx, 2)");
					setState(1372);
					_errHandler.sync(this);
					switch (_input.LA(1)) {
					case CROSS:
						{
						setState(1359);
						match(CROSS);
						setState(1360);
						match(JOIN);
						setState(1361);
						((JoinRelationContext)_localctx).right = sampledRelation();
						}
						break;
					case FULL:
					case INNER:
					case JOIN:
					case LEFT:
					case RIGHT:
						{
						setState(1362);
						joinType();
						setState(1363);
						match(JOIN);
						setState(1364);
						((JoinRelationContext)_localctx).rightRelation = relation(0);
						setState(1365);
						joinCriteria();
						}
						break;
					case NATURAL:
						{
						setState(1367);
						match(NATURAL);
						setState(1368);
						joinType();
						setState(1369);
						match(JOIN);
						setState(1370);
						((JoinRelationContext)_localctx).right = sampledRelation();
						}
						break;
					default:
						throw new NoViableAltException(this);
					}
					}
					} 
				}
				setState(1378);
				_errHandler.sync(this);
				_alt = getInterpreter().adaptivePredict(_input,175,_ctx);
			}
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			unrollRecursionContexts(_parentctx);
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class JoinTypeContext extends ParserRuleContext {
		public TerminalNode INNER() { return getToken(SqlBaseParser.INNER, 0); }
		public TerminalNode LEFT() { return getToken(SqlBaseParser.LEFT, 0); }
		public TerminalNode OUTER() { return getToken(SqlBaseParser.OUTER, 0); }
		public TerminalNode RIGHT() { return getToken(SqlBaseParser.RIGHT, 0); }
		public TerminalNode FULL() { return getToken(SqlBaseParser.FULL, 0); }
		public JoinTypeContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_joinType; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterJoinType(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitJoinType(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitJoinType(this);
			else return visitor.visitChildren(this);
		}
	}

	public final JoinTypeContext joinType() throws RecognitionException {
		JoinTypeContext _localctx = new JoinTypeContext(_ctx, getState());
		enterRule(_localctx, 64, RULE_joinType);
		int _la;
		try {
			setState(1394);
			_errHandler.sync(this);
			switch (_input.LA(1)) {
			case INNER:
			case JOIN:
				enterOuterAlt(_localctx, 1);
				{
				setState(1380);
				_errHandler.sync(this);
				_la = _input.LA(1);
				if (_la==INNER) {
					{
					setState(1379);
					match(INNER);
					}
				}

				}
				break;
			case LEFT:
				enterOuterAlt(_localctx, 2);
				{
				setState(1382);
				match(LEFT);
				setState(1384);
				_errHandler.sync(this);
				_la = _input.LA(1);
				if (_la==OUTER) {
					{
					setState(1383);
					match(OUTER);
					}
				}

				}
				break;
			case RIGHT:
				enterOuterAlt(_localctx, 3);
				{
				setState(1386);
				match(RIGHT);
				setState(1388);
				_errHandler.sync(this);
				_la = _input.LA(1);
				if (_la==OUTER) {
					{
					setState(1387);
					match(OUTER);
					}
				}

				}
				break;
			case FULL:
				enterOuterAlt(_localctx, 4);
				{
				setState(1390);
				match(FULL);
				setState(1392);
				_errHandler.sync(this);
				_la = _input.LA(1);
				if (_la==OUTER) {
					{
					setState(1391);
					match(OUTER);
					}
				}

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
	public static class JoinCriteriaContext extends ParserRuleContext {
		public TerminalNode ON() { return getToken(SqlBaseParser.ON, 0); }
		public BooleanExpressionContext booleanExpression() {
			return getRuleContext(BooleanExpressionContext.class,0);
		}
		public TerminalNode USING() { return getToken(SqlBaseParser.USING, 0); }
		public List<IdentifierContext> identifier() {
			return getRuleContexts(IdentifierContext.class);
		}
		public IdentifierContext identifier(int i) {
			return getRuleContext(IdentifierContext.class,i);
		}
		public JoinCriteriaContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_joinCriteria; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterJoinCriteria(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitJoinCriteria(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitJoinCriteria(this);
			else return visitor.visitChildren(this);
		}
	}

	public final JoinCriteriaContext joinCriteria() throws RecognitionException {
		JoinCriteriaContext _localctx = new JoinCriteriaContext(_ctx, getState());
		enterRule(_localctx, 66, RULE_joinCriteria);
		int _la;
		try {
			setState(1410);
			_errHandler.sync(this);
			switch (_input.LA(1)) {
			case ON:
				enterOuterAlt(_localctx, 1);
				{
				setState(1396);
				match(ON);
				setState(1397);
				booleanExpression(0);
				}
				break;
			case USING:
				enterOuterAlt(_localctx, 2);
				{
				setState(1398);
				match(USING);
				setState(1399);
				match(T__1);
				setState(1400);
				identifier();
				setState(1405);
				_errHandler.sync(this);
				_la = _input.LA(1);
				while (_la==T__3) {
					{
					{
					setState(1401);
					match(T__3);
					setState(1402);
					identifier();
					}
					}
					setState(1407);
					_errHandler.sync(this);
					_la = _input.LA(1);
				}
				setState(1408);
				match(T__2);
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
	public static class SampledRelationContext extends ParserRuleContext {
		public ExpressionContext percentage;
		public PatternRecognitionContext patternRecognition() {
			return getRuleContext(PatternRecognitionContext.class,0);
		}
		public TerminalNode TABLESAMPLE() { return getToken(SqlBaseParser.TABLESAMPLE, 0); }
		public SampleTypeContext sampleType() {
			return getRuleContext(SampleTypeContext.class,0);
		}
		public ExpressionContext expression() {
			return getRuleContext(ExpressionContext.class,0);
		}
		public SampledRelationContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_sampledRelation; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterSampledRelation(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitSampledRelation(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitSampledRelation(this);
			else return visitor.visitChildren(this);
		}
	}

	public final SampledRelationContext sampledRelation() throws RecognitionException {
		SampledRelationContext _localctx = new SampledRelationContext(_ctx, getState());
		enterRule(_localctx, 68, RULE_sampledRelation);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(1412);
			patternRecognition();
			setState(1419);
			_errHandler.sync(this);
			switch ( getInterpreter().adaptivePredict(_input,183,_ctx) ) {
			case 1:
				{
				setState(1413);
				match(TABLESAMPLE);
				setState(1414);
				sampleType();
				setState(1415);
				match(T__1);
				setState(1416);
				((SampledRelationContext)_localctx).percentage = expression();
				setState(1417);
				match(T__2);
				}
				break;
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
	public static class SampleTypeContext extends ParserRuleContext {
		public TerminalNode BERNOULLI() { return getToken(SqlBaseParser.BERNOULLI, 0); }
		public TerminalNode SYSTEM() { return getToken(SqlBaseParser.SYSTEM, 0); }
		public SampleTypeContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_sampleType; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterSampleType(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitSampleType(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitSampleType(this);
			else return visitor.visitChildren(this);
		}
	}

	public final SampleTypeContext sampleType() throws RecognitionException {
		SampleTypeContext _localctx = new SampleTypeContext(_ctx, getState());
		enterRule(_localctx, 70, RULE_sampleType);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(1421);
			_la = _input.LA(1);
			if ( !(_la==BERNOULLI || _la==SYSTEM) ) {
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

	@SuppressWarnings("CheckReturnValue")
	public static class ListAggOverflowBehaviorContext extends ParserRuleContext {
		public TerminalNode ERROR() { return getToken(SqlBaseParser.ERROR, 0); }
		public TerminalNode TRUNCATE() { return getToken(SqlBaseParser.TRUNCATE, 0); }
		public ListaggCountIndicationContext listaggCountIndication() {
			return getRuleContext(ListaggCountIndicationContext.class,0);
		}
		public StringContext string() {
			return getRuleContext(StringContext.class,0);
		}
		public ListAggOverflowBehaviorContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_listAggOverflowBehavior; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterListAggOverflowBehavior(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitListAggOverflowBehavior(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitListAggOverflowBehavior(this);
			else return visitor.visitChildren(this);
		}
	}

	public final ListAggOverflowBehaviorContext listAggOverflowBehavior() throws RecognitionException {
		ListAggOverflowBehaviorContext _localctx = new ListAggOverflowBehaviorContext(_ctx, getState());
		enterRule(_localctx, 72, RULE_listAggOverflowBehavior);
		int _la;
		try {
			setState(1429);
			_errHandler.sync(this);
			switch (_input.LA(1)) {
			case ERROR:
				enterOuterAlt(_localctx, 1);
				{
				setState(1423);
				match(ERROR);
				}
				break;
			case TRUNCATE:
				enterOuterAlt(_localctx, 2);
				{
				setState(1424);
				match(TRUNCATE);
				setState(1426);
				_errHandler.sync(this);
				_la = _input.LA(1);
				if (((((_la - 282)) & ~0x3f) == 0 && ((1L << (_la - 282)) & 32771L) != 0)) {
					{
					setState(1425);
					string();
					}
				}

				setState(1428);
				listaggCountIndication();
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
	public static class ListaggCountIndicationContext extends ParserRuleContext {
		public TerminalNode WITH() { return getToken(SqlBaseParser.WITH, 0); }
		public TerminalNode COUNT() { return getToken(SqlBaseParser.COUNT, 0); }
		public TerminalNode WITHOUT() { return getToken(SqlBaseParser.WITHOUT, 0); }
		public ListaggCountIndicationContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_listaggCountIndication; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterListaggCountIndication(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitListaggCountIndication(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitListaggCountIndication(this);
			else return visitor.visitChildren(this);
		}
	}

	public final ListaggCountIndicationContext listaggCountIndication() throws RecognitionException {
		ListaggCountIndicationContext _localctx = new ListaggCountIndicationContext(_ctx, getState());
		enterRule(_localctx, 74, RULE_listaggCountIndication);
		try {
			setState(1435);
			_errHandler.sync(this);
			switch (_input.LA(1)) {
			case WITH:
				enterOuterAlt(_localctx, 1);
				{
				setState(1431);
				match(WITH);
				setState(1432);
				match(COUNT);
				}
				break;
			case WITHOUT:
				enterOuterAlt(_localctx, 2);
				{
				setState(1433);
				match(WITHOUT);
				setState(1434);
				match(COUNT);
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
	public static class PatternRecognitionContext extends ParserRuleContext {
		public ExpressionContext expression;
		public List<ExpressionContext> partition = new ArrayList<ExpressionContext>();
		public AliasedRelationContext aliasedRelation() {
			return getRuleContext(AliasedRelationContext.class,0);
		}
		public TerminalNode MATCH_RECOGNIZE() { return getToken(SqlBaseParser.MATCH_RECOGNIZE, 0); }
		public TerminalNode PATTERN() { return getToken(SqlBaseParser.PATTERN, 0); }
		public RowPatternContext rowPattern() {
			return getRuleContext(RowPatternContext.class,0);
		}
		public TerminalNode DEFINE() { return getToken(SqlBaseParser.DEFINE, 0); }
		public List<VariableDefinitionContext> variableDefinition() {
			return getRuleContexts(VariableDefinitionContext.class);
		}
		public VariableDefinitionContext variableDefinition(int i) {
			return getRuleContext(VariableDefinitionContext.class,i);
		}
		public TerminalNode PARTITION() { return getToken(SqlBaseParser.PARTITION, 0); }
		public List<TerminalNode> BY() { return getTokens(SqlBaseParser.BY); }
		public TerminalNode BY(int i) {
			return getToken(SqlBaseParser.BY, i);
		}
		public TerminalNode ORDER() { return getToken(SqlBaseParser.ORDER, 0); }
		public List<SortItemContext> sortItem() {
			return getRuleContexts(SortItemContext.class);
		}
		public SortItemContext sortItem(int i) {
			return getRuleContext(SortItemContext.class,i);
		}
		public TerminalNode MEASURES() { return getToken(SqlBaseParser.MEASURES, 0); }
		public List<MeasureDefinitionContext> measureDefinition() {
			return getRuleContexts(MeasureDefinitionContext.class);
		}
		public MeasureDefinitionContext measureDefinition(int i) {
			return getRuleContext(MeasureDefinitionContext.class,i);
		}
		public RowsPerMatchContext rowsPerMatch() {
			return getRuleContext(RowsPerMatchContext.class,0);
		}
		public TerminalNode AFTER() { return getToken(SqlBaseParser.AFTER, 0); }
		public TerminalNode MATCH() { return getToken(SqlBaseParser.MATCH, 0); }
		public SkipToContext skipTo() {
			return getRuleContext(SkipToContext.class,0);
		}
		public TerminalNode SUBSET() { return getToken(SqlBaseParser.SUBSET, 0); }
		public List<SubsetDefinitionContext> subsetDefinition() {
			return getRuleContexts(SubsetDefinitionContext.class);
		}
		public SubsetDefinitionContext subsetDefinition(int i) {
			return getRuleContext(SubsetDefinitionContext.class,i);
		}
		public IdentifierContext identifier() {
			return getRuleContext(IdentifierContext.class,0);
		}
		public List<ExpressionContext> expression() {
			return getRuleContexts(ExpressionContext.class);
		}
		public ExpressionContext expression(int i) {
			return getRuleContext(ExpressionContext.class,i);
		}
		public TerminalNode INITIAL() { return getToken(SqlBaseParser.INITIAL, 0); }
		public TerminalNode SEEK() { return getToken(SqlBaseParser.SEEK, 0); }
		public TerminalNode AS() { return getToken(SqlBaseParser.AS, 0); }
		public ColumnAliasesContext columnAliases() {
			return getRuleContext(ColumnAliasesContext.class,0);
		}
		public PatternRecognitionContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_patternRecognition; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterPatternRecognition(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitPatternRecognition(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitPatternRecognition(this);
			else return visitor.visitChildren(this);
		}
	}

	public final PatternRecognitionContext patternRecognition() throws RecognitionException {
		PatternRecognitionContext _localctx = new PatternRecognitionContext(_ctx, getState());
		enterRule(_localctx, 76, RULE_patternRecognition);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(1437);
			aliasedRelation();
			setState(1520);
			_errHandler.sync(this);
			switch ( getInterpreter().adaptivePredict(_input,202,_ctx) ) {
			case 1:
				{
				setState(1438);
				match(MATCH_RECOGNIZE);
				setState(1439);
				match(T__1);
				setState(1450);
				_errHandler.sync(this);
				_la = _input.LA(1);
				if (_la==PARTITION) {
					{
					setState(1440);
					match(PARTITION);
					setState(1441);
					match(BY);
					setState(1442);
					((PatternRecognitionContext)_localctx).expression = expression();
					((PatternRecognitionContext)_localctx).partition.add(((PatternRecognitionContext)_localctx).expression);
					setState(1447);
					_errHandler.sync(this);
					_la = _input.LA(1);
					while (_la==T__3) {
						{
						{
						setState(1443);
						match(T__3);
						setState(1444);
						((PatternRecognitionContext)_localctx).expression = expression();
						((PatternRecognitionContext)_localctx).partition.add(((PatternRecognitionContext)_localctx).expression);
						}
						}
						setState(1449);
						_errHandler.sync(this);
						_la = _input.LA(1);
					}
					}
				}

				setState(1462);
				_errHandler.sync(this);
				_la = _input.LA(1);
				if (_la==ORDER) {
					{
					setState(1452);
					match(ORDER);
					setState(1453);
					match(BY);
					setState(1454);
					sortItem();
					setState(1459);
					_errHandler.sync(this);
					_la = _input.LA(1);
					while (_la==T__3) {
						{
						{
						setState(1455);
						match(T__3);
						setState(1456);
						sortItem();
						}
						}
						setState(1461);
						_errHandler.sync(this);
						_la = _input.LA(1);
					}
					}
				}

				setState(1473);
				_errHandler.sync(this);
				_la = _input.LA(1);
				if (_la==MEASURES) {
					{
					setState(1464);
					match(MEASURES);
					setState(1465);
					measureDefinition();
					setState(1470);
					_errHandler.sync(this);
					_la = _input.LA(1);
					while (_la==T__3) {
						{
						{
						setState(1466);
						match(T__3);
						setState(1467);
						measureDefinition();
						}
						}
						setState(1472);
						_errHandler.sync(this);
						_la = _input.LA(1);
					}
					}
				}

				setState(1476);
				_errHandler.sync(this);
				_la = _input.LA(1);
				if (_la==ALL || _la==ONE) {
					{
					setState(1475);
					rowsPerMatch();
					}
				}

				setState(1481);
				_errHandler.sync(this);
				_la = _input.LA(1);
				if (_la==AFTER) {
					{
					setState(1478);
					match(AFTER);
					setState(1479);
					match(MATCH);
					setState(1480);
					skipTo();
					}
				}

				setState(1484);
				_errHandler.sync(this);
				_la = _input.LA(1);
				if (_la==INITIAL || _la==SEEK) {
					{
					setState(1483);
					_la = _input.LA(1);
					if ( !(_la==INITIAL || _la==SEEK) ) {
					_errHandler.recoverInline(this);
					}
					else {
						if ( _input.LA(1)==Token.EOF ) matchedEOF = true;
						_errHandler.reportMatch(this);
						consume();
					}
					}
				}

				setState(1486);
				match(PATTERN);
				setState(1487);
				match(T__1);
				setState(1488);
				rowPattern(0);
				setState(1489);
				match(T__2);
				setState(1499);
				_errHandler.sync(this);
				_la = _input.LA(1);
				if (_la==SUBSET) {
					{
					setState(1490);
					match(SUBSET);
					setState(1491);
					subsetDefinition();
					setState(1496);
					_errHandler.sync(this);
					_la = _input.LA(1);
					while (_la==T__3) {
						{
						{
						setState(1492);
						match(T__3);
						setState(1493);
						subsetDefinition();
						}
						}
						setState(1498);
						_errHandler.sync(this);
						_la = _input.LA(1);
					}
					}
				}

				setState(1501);
				match(DEFINE);
				setState(1502);
				variableDefinition();
				setState(1507);
				_errHandler.sync(this);
				_la = _input.LA(1);
				while (_la==T__3) {
					{
					{
					setState(1503);
					match(T__3);
					setState(1504);
					variableDefinition();
					}
					}
					setState(1509);
					_errHandler.sync(this);
					_la = _input.LA(1);
				}
				setState(1510);
				match(T__2);
				setState(1518);
				_errHandler.sync(this);
				switch ( getInterpreter().adaptivePredict(_input,201,_ctx) ) {
				case 1:
					{
					setState(1512);
					_errHandler.sync(this);
					_la = _input.LA(1);
					if (_la==AS) {
						{
						setState(1511);
						match(AS);
						}
					}

					setState(1514);
					identifier();
					setState(1516);
					_errHandler.sync(this);
					switch ( getInterpreter().adaptivePredict(_input,200,_ctx) ) {
					case 1:
						{
						setState(1515);
						columnAliases();
						}
						break;
					}
					}
					break;
				}
				}
				break;
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
	public static class MeasureDefinitionContext extends ParserRuleContext {
		public ExpressionContext expression() {
			return getRuleContext(ExpressionContext.class,0);
		}
		public TerminalNode AS() { return getToken(SqlBaseParser.AS, 0); }
		public IdentifierContext identifier() {
			return getRuleContext(IdentifierContext.class,0);
		}
		public MeasureDefinitionContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_measureDefinition; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterMeasureDefinition(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitMeasureDefinition(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitMeasureDefinition(this);
			else return visitor.visitChildren(this);
		}
	}

	public final MeasureDefinitionContext measureDefinition() throws RecognitionException {
		MeasureDefinitionContext _localctx = new MeasureDefinitionContext(_ctx, getState());
		enterRule(_localctx, 78, RULE_measureDefinition);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(1522);
			expression();
			setState(1523);
			match(AS);
			setState(1524);
			identifier();
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
	public static class RowsPerMatchContext extends ParserRuleContext {
		public TerminalNode ONE() { return getToken(SqlBaseParser.ONE, 0); }
		public TerminalNode ROW() { return getToken(SqlBaseParser.ROW, 0); }
		public TerminalNode PER() { return getToken(SqlBaseParser.PER, 0); }
		public TerminalNode MATCH() { return getToken(SqlBaseParser.MATCH, 0); }
		public TerminalNode ALL() { return getToken(SqlBaseParser.ALL, 0); }
		public TerminalNode ROWS() { return getToken(SqlBaseParser.ROWS, 0); }
		public EmptyMatchHandlingContext emptyMatchHandling() {
			return getRuleContext(EmptyMatchHandlingContext.class,0);
		}
		public RowsPerMatchContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_rowsPerMatch; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterRowsPerMatch(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitRowsPerMatch(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitRowsPerMatch(this);
			else return visitor.visitChildren(this);
		}
	}

	public final RowsPerMatchContext rowsPerMatch() throws RecognitionException {
		RowsPerMatchContext _localctx = new RowsPerMatchContext(_ctx, getState());
		enterRule(_localctx, 80, RULE_rowsPerMatch);
		int _la;
		try {
			setState(1537);
			_errHandler.sync(this);
			switch (_input.LA(1)) {
			case ONE:
				enterOuterAlt(_localctx, 1);
				{
				setState(1526);
				match(ONE);
				setState(1527);
				match(ROW);
				setState(1528);
				match(PER);
				setState(1529);
				match(MATCH);
				}
				break;
			case ALL:
				enterOuterAlt(_localctx, 2);
				{
				setState(1530);
				match(ALL);
				setState(1531);
				match(ROWS);
				setState(1532);
				match(PER);
				setState(1533);
				match(MATCH);
				setState(1535);
				_errHandler.sync(this);
				_la = _input.LA(1);
				if (_la==OMIT || _la==SHOW || _la==WITH) {
					{
					setState(1534);
					emptyMatchHandling();
					}
				}

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
	public static class EmptyMatchHandlingContext extends ParserRuleContext {
		public TerminalNode SHOW() { return getToken(SqlBaseParser.SHOW, 0); }
		public TerminalNode EMPTY() { return getToken(SqlBaseParser.EMPTY, 0); }
		public TerminalNode MATCHES() { return getToken(SqlBaseParser.MATCHES, 0); }
		public TerminalNode OMIT() { return getToken(SqlBaseParser.OMIT, 0); }
		public TerminalNode WITH() { return getToken(SqlBaseParser.WITH, 0); }
		public TerminalNode UNMATCHED() { return getToken(SqlBaseParser.UNMATCHED, 0); }
		public TerminalNode ROWS() { return getToken(SqlBaseParser.ROWS, 0); }
		public EmptyMatchHandlingContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_emptyMatchHandling; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterEmptyMatchHandling(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitEmptyMatchHandling(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitEmptyMatchHandling(this);
			else return visitor.visitChildren(this);
		}
	}

	public final EmptyMatchHandlingContext emptyMatchHandling() throws RecognitionException {
		EmptyMatchHandlingContext _localctx = new EmptyMatchHandlingContext(_ctx, getState());
		enterRule(_localctx, 82, RULE_emptyMatchHandling);
		try {
			setState(1548);
			_errHandler.sync(this);
			switch (_input.LA(1)) {
			case SHOW:
				enterOuterAlt(_localctx, 1);
				{
				setState(1539);
				match(SHOW);
				setState(1540);
				match(EMPTY);
				setState(1541);
				match(MATCHES);
				}
				break;
			case OMIT:
				enterOuterAlt(_localctx, 2);
				{
				setState(1542);
				match(OMIT);
				setState(1543);
				match(EMPTY);
				setState(1544);
				match(MATCHES);
				}
				break;
			case WITH:
				enterOuterAlt(_localctx, 3);
				{
				setState(1545);
				match(WITH);
				setState(1546);
				match(UNMATCHED);
				setState(1547);
				match(ROWS);
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
	public static class SkipToContext extends ParserRuleContext {
		public TerminalNode TO() { return getToken(SqlBaseParser.TO, 0); }
		public TerminalNode NEXT() { return getToken(SqlBaseParser.NEXT, 0); }
		public TerminalNode ROW() { return getToken(SqlBaseParser.ROW, 0); }
		public TerminalNode PAST() { return getToken(SqlBaseParser.PAST, 0); }
		public TerminalNode LAST() { return getToken(SqlBaseParser.LAST, 0); }
		public TerminalNode FIRST() { return getToken(SqlBaseParser.FIRST, 0); }
		public IdentifierContext identifier() {
			return getRuleContext(IdentifierContext.class,0);
		}
		public SkipToContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_skipTo; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterSkipTo(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitSkipTo(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitSkipTo(this);
			else return visitor.visitChildren(this);
		}
	}

	public final SkipToContext skipTo() throws RecognitionException {
		SkipToContext _localctx = new SkipToContext(_ctx, getState());
		enterRule(_localctx, 84, RULE_skipTo);
		try {
			setState(1569);
			_errHandler.sync(this);
			switch ( getInterpreter().adaptivePredict(_input,206,_ctx) ) {
			case 1:
				enterOuterAlt(_localctx, 1);
				{
				setState(1550);
				match(T__9);
				setState(1551);
				match(TO);
				setState(1552);
				match(NEXT);
				setState(1553);
				match(ROW);
				}
				break;
			case 2:
				enterOuterAlt(_localctx, 2);
				{
				setState(1554);
				match(T__9);
				setState(1555);
				match(PAST);
				setState(1556);
				match(LAST);
				setState(1557);
				match(ROW);
				}
				break;
			case 3:
				enterOuterAlt(_localctx, 3);
				{
				setState(1558);
				match(T__9);
				setState(1559);
				match(TO);
				setState(1560);
				match(FIRST);
				setState(1561);
				identifier();
				}
				break;
			case 4:
				enterOuterAlt(_localctx, 4);
				{
				setState(1562);
				match(T__9);
				setState(1563);
				match(TO);
				setState(1564);
				match(LAST);
				setState(1565);
				identifier();
				}
				break;
			case 5:
				enterOuterAlt(_localctx, 5);
				{
				setState(1566);
				match(T__9);
				setState(1567);
				match(TO);
				setState(1568);
				identifier();
				}
				break;
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
	public static class SubsetDefinitionContext extends ParserRuleContext {
		public IdentifierContext name;
		public IdentifierContext identifier;
		public List<IdentifierContext> union = new ArrayList<IdentifierContext>();
		public TerminalNode EQ() { return getToken(SqlBaseParser.EQ, 0); }
		public List<IdentifierContext> identifier() {
			return getRuleContexts(IdentifierContext.class);
		}
		public IdentifierContext identifier(int i) {
			return getRuleContext(IdentifierContext.class,i);
		}
		public SubsetDefinitionContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_subsetDefinition; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterSubsetDefinition(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitSubsetDefinition(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitSubsetDefinition(this);
			else return visitor.visitChildren(this);
		}
	}

	public final SubsetDefinitionContext subsetDefinition() throws RecognitionException {
		SubsetDefinitionContext _localctx = new SubsetDefinitionContext(_ctx, getState());
		enterRule(_localctx, 86, RULE_subsetDefinition);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(1571);
			((SubsetDefinitionContext)_localctx).name = identifier();
			setState(1572);
			match(EQ);
			setState(1573);
			match(T__1);
			setState(1574);
			((SubsetDefinitionContext)_localctx).identifier = identifier();
			((SubsetDefinitionContext)_localctx).union.add(((SubsetDefinitionContext)_localctx).identifier);
			setState(1579);
			_errHandler.sync(this);
			_la = _input.LA(1);
			while (_la==T__3) {
				{
				{
				setState(1575);
				match(T__3);
				setState(1576);
				((SubsetDefinitionContext)_localctx).identifier = identifier();
				((SubsetDefinitionContext)_localctx).union.add(((SubsetDefinitionContext)_localctx).identifier);
				}
				}
				setState(1581);
				_errHandler.sync(this);
				_la = _input.LA(1);
			}
			setState(1582);
			match(T__2);
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
	public static class VariableDefinitionContext extends ParserRuleContext {
		public IdentifierContext identifier() {
			return getRuleContext(IdentifierContext.class,0);
		}
		public TerminalNode AS() { return getToken(SqlBaseParser.AS, 0); }
		public ExpressionContext expression() {
			return getRuleContext(ExpressionContext.class,0);
		}
		public VariableDefinitionContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_variableDefinition; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterVariableDefinition(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitVariableDefinition(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitVariableDefinition(this);
			else return visitor.visitChildren(this);
		}
	}

	public final VariableDefinitionContext variableDefinition() throws RecognitionException {
		VariableDefinitionContext _localctx = new VariableDefinitionContext(_ctx, getState());
		enterRule(_localctx, 88, RULE_variableDefinition);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(1584);
			identifier();
			setState(1585);
			match(AS);
			setState(1586);
			expression();
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
	public static class AliasedRelationContext extends ParserRuleContext {
		public RelationPrimaryContext relationPrimary() {
			return getRuleContext(RelationPrimaryContext.class,0);
		}
		public IdentifierContext identifier() {
			return getRuleContext(IdentifierContext.class,0);
		}
		public TerminalNode AS() { return getToken(SqlBaseParser.AS, 0); }
		public ColumnAliasesContext columnAliases() {
			return getRuleContext(ColumnAliasesContext.class,0);
		}
		public AliasedRelationContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_aliasedRelation; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterAliasedRelation(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitAliasedRelation(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitAliasedRelation(this);
			else return visitor.visitChildren(this);
		}
	}

	public final AliasedRelationContext aliasedRelation() throws RecognitionException {
		AliasedRelationContext _localctx = new AliasedRelationContext(_ctx, getState());
		enterRule(_localctx, 90, RULE_aliasedRelation);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(1588);
			relationPrimary();
			setState(1596);
			_errHandler.sync(this);
			switch ( getInterpreter().adaptivePredict(_input,210,_ctx) ) {
			case 1:
				{
				setState(1590);
				_errHandler.sync(this);
				_la = _input.LA(1);
				if (_la==AS) {
					{
					setState(1589);
					match(AS);
					}
				}

				setState(1592);
				identifier();
				setState(1594);
				_errHandler.sync(this);
				switch ( getInterpreter().adaptivePredict(_input,209,_ctx) ) {
				case 1:
					{
					setState(1593);
					columnAliases();
					}
					break;
				}
				}
				break;
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
	public static class ColumnAliasesContext extends ParserRuleContext {
		public List<IdentifierContext> identifier() {
			return getRuleContexts(IdentifierContext.class);
		}
		public IdentifierContext identifier(int i) {
			return getRuleContext(IdentifierContext.class,i);
		}
		public ColumnAliasesContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_columnAliases; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterColumnAliases(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitColumnAliases(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitColumnAliases(this);
			else return visitor.visitChildren(this);
		}
	}

	public final ColumnAliasesContext columnAliases() throws RecognitionException {
		ColumnAliasesContext _localctx = new ColumnAliasesContext(_ctx, getState());
		enterRule(_localctx, 92, RULE_columnAliases);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(1598);
			match(T__1);
			setState(1599);
			identifier();
			setState(1604);
			_errHandler.sync(this);
			_la = _input.LA(1);
			while (_la==T__3) {
				{
				{
				setState(1600);
				match(T__3);
				setState(1601);
				identifier();
				}
				}
				setState(1606);
				_errHandler.sync(this);
				_la = _input.LA(1);
			}
			setState(1607);
			match(T__2);
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
	public static class RelationPrimaryContext extends ParserRuleContext {
		public RelationPrimaryContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_relationPrimary; }
	 
		public RelationPrimaryContext() { }
		public void copyFrom(RelationPrimaryContext ctx) {
			super.copyFrom(ctx);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class PathRelationContext extends RelationPrimaryContext {
		public StringContext string() {
			return getRuleContext(StringContext.class,0);
		}
		public PathRelationContext(RelationPrimaryContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterPathRelation(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitPathRelation(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitPathRelation(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class SubqueryRelationContext extends RelationPrimaryContext {
		public QueryContext query() {
			return getRuleContext(QueryContext.class,0);
		}
		public SubqueryRelationContext(RelationPrimaryContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterSubqueryRelation(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitSubqueryRelation(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitSubqueryRelation(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class ParenthesizedRelationContext extends RelationPrimaryContext {
		public RelationContext relation() {
			return getRuleContext(RelationContext.class,0);
		}
		public ParenthesizedRelationContext(RelationPrimaryContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterParenthesizedRelation(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitParenthesizedRelation(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitParenthesizedRelation(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class UnnestContext extends RelationPrimaryContext {
		public TerminalNode UNNEST() { return getToken(SqlBaseParser.UNNEST, 0); }
		public List<ExpressionContext> expression() {
			return getRuleContexts(ExpressionContext.class);
		}
		public ExpressionContext expression(int i) {
			return getRuleContext(ExpressionContext.class,i);
		}
		public TerminalNode WITH() { return getToken(SqlBaseParser.WITH, 0); }
		public TerminalNode ORDINALITY() { return getToken(SqlBaseParser.ORDINALITY, 0); }
		public TerminalNode IDENTIFIER() { return getToken(SqlBaseParser.IDENTIFIER, 0); }
		public UnnestContext(RelationPrimaryContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterUnnest(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitUnnest(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitUnnest(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class FunctionRelationContext extends RelationPrimaryContext {
		public FunctionExpressionContext functionExpression() {
			return getRuleContext(FunctionExpressionContext.class,0);
		}
		public FunctionRelationContext(RelationPrimaryContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterFunctionRelation(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitFunctionRelation(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitFunctionRelation(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class LateralContext extends RelationPrimaryContext {
		public TerminalNode LATERAL() { return getToken(SqlBaseParser.LATERAL, 0); }
		public QueryContext query() {
			return getRuleContext(QueryContext.class,0);
		}
		public LateralContext(RelationPrimaryContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterLateral(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitLateral(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitLateral(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class TableNameContext extends RelationPrimaryContext {
		public QualifiedNameContext qualifiedName() {
			return getRuleContext(QualifiedNameContext.class,0);
		}
		public QueryPeriodContext queryPeriod() {
			return getRuleContext(QueryPeriodContext.class,0);
		}
		public TableNameContext(RelationPrimaryContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterTableName(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitTableName(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitTableName(this);
			else return visitor.visitChildren(this);
		}
	}

	public final RelationPrimaryContext relationPrimary() throws RecognitionException {
		RelationPrimaryContext _localctx = new RelationPrimaryContext(_ctx, getState());
		enterRule(_localctx, 94, RULE_relationPrimary);
		int _la;
		try {
			setState(1662);
			_errHandler.sync(this);
			switch ( getInterpreter().adaptivePredict(_input,218,_ctx) ) {
			case 1:
				_localctx = new TableNameContext(_localctx);
				enterOuterAlt(_localctx, 1);
				{
				setState(1609);
				qualifiedName();
				setState(1611);
				_errHandler.sync(this);
				switch ( getInterpreter().adaptivePredict(_input,212,_ctx) ) {
				case 1:
					{
					setState(1610);
					queryPeriod();
					}
					break;
				}
				}
				break;
			case 2:
				_localctx = new SubqueryRelationContext(_localctx);
				enterOuterAlt(_localctx, 2);
				{
				setState(1613);
				match(T__1);
				setState(1614);
				query();
				setState(1615);
				match(T__2);
				}
				break;
			case 3:
				_localctx = new UnnestContext(_localctx);
				enterOuterAlt(_localctx, 3);
				{
				setState(1617);
				match(UNNEST);
				setState(1618);
				match(T__1);
				setState(1619);
				expression();
				setState(1624);
				_errHandler.sync(this);
				_la = _input.LA(1);
				while (_la==T__3) {
					{
					{
					setState(1620);
					match(T__3);
					setState(1621);
					expression();
					}
					}
					setState(1626);
					_errHandler.sync(this);
					_la = _input.LA(1);
				}
				setState(1627);
				match(T__2);
				setState(1630);
				_errHandler.sync(this);
				switch ( getInterpreter().adaptivePredict(_input,214,_ctx) ) {
				case 1:
					{
					setState(1628);
					match(WITH);
					setState(1629);
					match(ORDINALITY);
					}
					break;
				}
				}
				break;
			case 4:
				_localctx = new UnnestContext(_localctx);
				enterOuterAlt(_localctx, 4);
				{
				setState(1634);
				_errHandler.sync(this);
				_la = _input.LA(1);
				if (_la==IDENTIFIER) {
					{
					setState(1632);
					match(IDENTIFIER);
					setState(1633);
					match(T__0);
					}
				}

				setState(1636);
				match(UNNEST);
				setState(1637);
				match(T__1);
				setState(1638);
				expression();
				setState(1643);
				_errHandler.sync(this);
				_la = _input.LA(1);
				while (_la==T__3) {
					{
					{
					setState(1639);
					match(T__3);
					setState(1640);
					expression();
					}
					}
					setState(1645);
					_errHandler.sync(this);
					_la = _input.LA(1);
				}
				setState(1646);
				match(T__2);
				setState(1649);
				_errHandler.sync(this);
				switch ( getInterpreter().adaptivePredict(_input,217,_ctx) ) {
				case 1:
					{
					setState(1647);
					match(WITH);
					setState(1648);
					match(ORDINALITY);
					}
					break;
				}
				}
				break;
			case 5:
				_localctx = new FunctionRelationContext(_localctx);
				enterOuterAlt(_localctx, 5);
				{
				setState(1651);
				functionExpression();
				}
				break;
			case 6:
				_localctx = new PathRelationContext(_localctx);
				enterOuterAlt(_localctx, 6);
				{
				setState(1652);
				string();
				}
				break;
			case 7:
				_localctx = new LateralContext(_localctx);
				enterOuterAlt(_localctx, 7);
				{
				setState(1653);
				match(LATERAL);
				setState(1654);
				match(T__1);
				setState(1655);
				query();
				setState(1656);
				match(T__2);
				}
				break;
			case 8:
				_localctx = new ParenthesizedRelationContext(_localctx);
				enterOuterAlt(_localctx, 8);
				{
				setState(1658);
				match(T__1);
				setState(1659);
				relation(0);
				setState(1660);
				match(T__2);
				}
				break;
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
	public static class ExpressionContext extends ParserRuleContext {
		public BooleanExpressionContext booleanExpression() {
			return getRuleContext(BooleanExpressionContext.class,0);
		}
		public ExpressionContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_expression; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterExpression(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitExpression(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitExpression(this);
			else return visitor.visitChildren(this);
		}
	}

	public final ExpressionContext expression() throws RecognitionException {
		ExpressionContext _localctx = new ExpressionContext(_ctx, getState());
		enterRule(_localctx, 96, RULE_expression);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(1664);
			booleanExpression(0);
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
	public static class BooleanExpressionContext extends ParserRuleContext {
		public BooleanExpressionContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_booleanExpression; }
	 
		public BooleanExpressionContext() { }
		public void copyFrom(BooleanExpressionContext ctx) {
			super.copyFrom(ctx);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class LogicalNotContext extends BooleanExpressionContext {
		public TerminalNode NOT() { return getToken(SqlBaseParser.NOT, 0); }
		public BooleanExpressionContext booleanExpression() {
			return getRuleContext(BooleanExpressionContext.class,0);
		}
		public LogicalNotContext(BooleanExpressionContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterLogicalNot(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitLogicalNot(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitLogicalNot(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class PredicatedContext extends BooleanExpressionContext {
		public ValueExpressionContext valueExpression;
		public ValueExpressionContext valueExpression() {
			return getRuleContext(ValueExpressionContext.class,0);
		}
		public PredicateContext predicate() {
			return getRuleContext(PredicateContext.class,0);
		}
		public PredicatedContext(BooleanExpressionContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterPredicated(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitPredicated(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitPredicated(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class OrContext extends BooleanExpressionContext {
		public List<BooleanExpressionContext> booleanExpression() {
			return getRuleContexts(BooleanExpressionContext.class);
		}
		public BooleanExpressionContext booleanExpression(int i) {
			return getRuleContext(BooleanExpressionContext.class,i);
		}
		public TerminalNode OR() { return getToken(SqlBaseParser.OR, 0); }
		public OrContext(BooleanExpressionContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterOr(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitOr(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitOr(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class AndContext extends BooleanExpressionContext {
		public List<BooleanExpressionContext> booleanExpression() {
			return getRuleContexts(BooleanExpressionContext.class);
		}
		public BooleanExpressionContext booleanExpression(int i) {
			return getRuleContext(BooleanExpressionContext.class,i);
		}
		public TerminalNode AND() { return getToken(SqlBaseParser.AND, 0); }
		public AndContext(BooleanExpressionContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterAnd(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitAnd(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitAnd(this);
			else return visitor.visitChildren(this);
		}
	}

	public final BooleanExpressionContext booleanExpression() throws RecognitionException {
		return booleanExpression(0);
	}

	private BooleanExpressionContext booleanExpression(int _p) throws RecognitionException {
		ParserRuleContext _parentctx = _ctx;
		int _parentState = getState();
		BooleanExpressionContext _localctx = new BooleanExpressionContext(_ctx, _parentState);
		BooleanExpressionContext _prevctx = _localctx;
		int _startState = 98;
		enterRecursionRule(_localctx, 98, RULE_booleanExpression, _p);
		try {
			int _alt;
			enterOuterAlt(_localctx, 1);
			{
			setState(1673);
			_errHandler.sync(this);
			switch (_input.LA(1)) {
			case T__1:
			case T__11:
			case ADD:
			case ADMIN:
			case AFTER:
			case ALL:
			case ANALYZE:
			case ANY:
			case ARRAY:
			case ASC:
			case AT:
			case AUTHORIZATION:
			case BERNOULLI:
			case CALL:
			case CASCADE:
			case CASE:
			case CAST:
			case CATALOGS:
			case COLLATE:
			case COLUMN:
			case COLUMNS:
			case COMMENT:
			case COMMIT:
			case COMMITTED:
			case COUNT:
			case CURRENT:
			case CURRENT_CATALOG:
			case CURRENT_DATE:
			case CURRENT_PATH:
			case CURRENT_SCHEMA:
			case CURRENT_TIME:
			case CURRENT_TIMESTAMP:
			case CURRENT_USER:
			case CURSOR:
			case DATA:
			case DATE:
			case DAY:
			case DECLARE:
			case DEFAULT:
			case DEFINER:
			case DENY:
			case DESC:
			case DEFINE:
			case DISTRIBUTED:
			case DOUBLE:
			case EMPTY:
			case EPOCH:
			case ERROR:
			case EXCLUDING:
			case EXISTS:
			case EXPLAIN:
			case EXTRACT:
			case FALSE:
			case FETCH:
			case FILTER:
			case FINAL:
			case FIRST:
			case FOLLOWING:
			case FORMAT:
			case FUNCTIONS:
			case GRANT:
			case GRANTED:
			case GRANTS:
			case GRAPHVIZ:
			case GROUPING:
			case GROUPS:
			case HOUR:
			case IF:
			case IGNORE:
			case IMPERSONATE:
			case INCLUDING:
			case INITIAL:
			case INPUT:
			case INTERVAL:
			case INVOKER:
			case IO:
			case ISOLATION:
			case JSON:
			case LAST:
			case LATERAL:
			case LEVEL:
			case LIMIT:
			case LISTAGG:
			case LOCAL:
			case LOCALTIME:
			case LOCALTIMESTAMP:
			case LOGICAL:
			case MAP:
			case MATCH:
			case MATCHED:
			case MATCHES:
			case MATCH_RECOGNIZE:
			case MATERIALIZED:
			case MEASURES:
			case MERGE:
			case MINUTE:
			case MONTH:
			case NEXT:
			case NFC:
			case NFD:
			case NFKC:
			case NFKD:
			case NO:
			case NONE:
			case NORMALIZE:
			case NULL:
			case NULLIF:
			case NULLS:
			case OFFSET:
			case OMIT:
			case OF:
			case ONE:
			case ONLY:
			case OPERATOR:
			case OPTION:
			case ORDINALITY:
			case OUTPUT:
			case OVER:
			case OVERFLOW:
			case PARTITION:
			case PARTITIONS:
			case PAST:
			case PATH:
			case PATTERN:
			case PER:
			case PERMUTE:
			case POSITION:
			case PRECEDING:
			case PRECISION:
			case PRIVILEGES:
			case PROPERTIES:
			case RANGE:
			case READ:
			case REFRESH:
			case RENAME:
			case REPEATABLE:
			case REPLACE:
			case RESET:
			case RESPECT:
			case RESTRICT:
			case REVOKE:
			case ROLE:
			case ROLES:
			case ROLLBACK:
			case ROW:
			case ROWS:
			case RUNNING:
			case SCHEMA:
			case SCHEMAS:
			case SECOND:
			case SECURITY:
			case SEEK:
			case SERIALIZABLE:
			case SESSION:
			case SESSION_USER:
			case SET:
			case SETS:
			case SHOW:
			case SOME:
			case START:
			case STATS:
			case SUBSET:
			case SUBSTRING:
			case SYSTEM:
			case TABLES:
			case TABLESAMPLE:
			case TEXT:
			case TIES:
			case TIME:
			case TIMESTAMP:
			case TO:
			case TRANSACTION:
			case TRUE:
			case TRUNCATE:
			case TRY_CAST:
			case TYPE:
			case UNBOUNDED:
			case UNCOMMITTED:
			case UNMATCHED:
			case UPDATE:
			case USE:
			case USER:
			case VALIDATE:
			case VERBOSE:
			case VERSION:
			case VIEW:
			case WINDOW:
			case WITHIN:
			case WITHOUT:
			case WORK:
			case WRITE:
			case YEAR:
			case ZONE:
			case PLUS:
			case MINUS:
			case QUESTION_MARK:
			case STRING:
			case UNICODE_STRING:
			case BINARY_LITERAL:
			case INTEGER_VALUE:
			case DECIMAL_VALUE:
			case DOUBLE_VALUE:
			case IDENTIFIER:
			case DIGIT_IDENTIFIER:
			case QUOTED_IDENTIFIER:
			case BACKQUOTED_IDENTIFIER:
			case ESCAPED_STRING:
				{
				_localctx = new PredicatedContext(_localctx);
				_ctx = _localctx;
				_prevctx = _localctx;

				setState(1667);
				((PredicatedContext)_localctx).valueExpression = valueExpression(0);
				setState(1669);
				_errHandler.sync(this);
				switch ( getInterpreter().adaptivePredict(_input,219,_ctx) ) {
				case 1:
					{
					setState(1668);
					predicate(((PredicatedContext)_localctx).valueExpression);
					}
					break;
				}
				}
				break;
			case NOT:
				{
				_localctx = new LogicalNotContext(_localctx);
				_ctx = _localctx;
				_prevctx = _localctx;
				setState(1671);
				match(NOT);
				setState(1672);
				booleanExpression(3);
				}
				break;
			default:
				throw new NoViableAltException(this);
			}
			_ctx.stop = _input.LT(-1);
			setState(1683);
			_errHandler.sync(this);
			_alt = getInterpreter().adaptivePredict(_input,222,_ctx);
			while ( _alt!=2 && _alt!=org.antlr.v4.runtime.atn.ATN.INVALID_ALT_NUMBER ) {
				if ( _alt==1 ) {
					if ( _parseListeners!=null ) triggerExitRuleEvent();
					_prevctx = _localctx;
					{
					setState(1681);
					_errHandler.sync(this);
					switch ( getInterpreter().adaptivePredict(_input,221,_ctx) ) {
					case 1:
						{
						_localctx = new AndContext(new BooleanExpressionContext(_parentctx, _parentState));
						pushNewRecursionContext(_localctx, _startState, RULE_booleanExpression);
						setState(1675);
						if (!(precpred(_ctx, 2))) throw new FailedPredicateException(this, "precpred(_ctx, 2)");
						setState(1676);
						match(AND);
						setState(1677);
						booleanExpression(3);
						}
						break;
					case 2:
						{
						_localctx = new OrContext(new BooleanExpressionContext(_parentctx, _parentState));
						pushNewRecursionContext(_localctx, _startState, RULE_booleanExpression);
						setState(1678);
						if (!(precpred(_ctx, 1))) throw new FailedPredicateException(this, "precpred(_ctx, 1)");
						setState(1679);
						match(OR);
						setState(1680);
						booleanExpression(2);
						}
						break;
					}
					} 
				}
				setState(1685);
				_errHandler.sync(this);
				_alt = getInterpreter().adaptivePredict(_input,222,_ctx);
			}
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			unrollRecursionContexts(_parentctx);
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class PredicateContext extends ParserRuleContext {
		public ParserRuleContext value;
		public PredicateContext(ParserRuleContext parent, int invokingState) { super(parent, invokingState); }
		public PredicateContext(ParserRuleContext parent, int invokingState, ParserRuleContext value) {
			super(parent, invokingState);
			this.value = value;
		}
		@Override public int getRuleIndex() { return RULE_predicate; }
	 
		public PredicateContext() { }
		public void copyFrom(PredicateContext ctx) {
			super.copyFrom(ctx);
			this.value = ctx.value;
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class ComparisonContext extends PredicateContext {
		public ValueExpressionContext right;
		public TerminalNode OPERATOR() { return getToken(SqlBaseParser.OPERATOR, 0); }
		public ComparisonOperatorContext comparisonOperator() {
			return getRuleContext(ComparisonOperatorContext.class,0);
		}
		public ValueExpressionContext valueExpression() {
			return getRuleContext(ValueExpressionContext.class,0);
		}
		public TerminalNode IDENTIFIER() { return getToken(SqlBaseParser.IDENTIFIER, 0); }
		public ComparisonContext(PredicateContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterComparison(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitComparison(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitComparison(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class LikeContext extends PredicateContext {
		public ValueExpressionContext pattern;
		public ValueExpressionContext escape;
		public TerminalNode LIKE() { return getToken(SqlBaseParser.LIKE, 0); }
		public List<ValueExpressionContext> valueExpression() {
			return getRuleContexts(ValueExpressionContext.class);
		}
		public ValueExpressionContext valueExpression(int i) {
			return getRuleContext(ValueExpressionContext.class,i);
		}
		public TerminalNode NOT() { return getToken(SqlBaseParser.NOT, 0); }
		public TerminalNode ESCAPE() { return getToken(SqlBaseParser.ESCAPE, 0); }
		public LikeContext(PredicateContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterLike(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitLike(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitLike(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class InSubqueryContext extends PredicateContext {
		public TerminalNode IN() { return getToken(SqlBaseParser.IN, 0); }
		public QueryContext query() {
			return getRuleContext(QueryContext.class,0);
		}
		public TerminalNode NOT() { return getToken(SqlBaseParser.NOT, 0); }
		public InSubqueryContext(PredicateContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterInSubquery(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitInSubquery(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitInSubquery(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class DistinctFromContext extends PredicateContext {
		public ValueExpressionContext right;
		public TerminalNode IS() { return getToken(SqlBaseParser.IS, 0); }
		public TerminalNode DISTINCT() { return getToken(SqlBaseParser.DISTINCT, 0); }
		public TerminalNode FROM() { return getToken(SqlBaseParser.FROM, 0); }
		public ValueExpressionContext valueExpression() {
			return getRuleContext(ValueExpressionContext.class,0);
		}
		public TerminalNode NOT() { return getToken(SqlBaseParser.NOT, 0); }
		public DistinctFromContext(PredicateContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterDistinctFrom(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitDistinctFrom(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitDistinctFrom(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class InListContext extends PredicateContext {
		public TerminalNode IN() { return getToken(SqlBaseParser.IN, 0); }
		public List<ExpressionContext> expression() {
			return getRuleContexts(ExpressionContext.class);
		}
		public ExpressionContext expression(int i) {
			return getRuleContext(ExpressionContext.class,i);
		}
		public TerminalNode NOT() { return getToken(SqlBaseParser.NOT, 0); }
		public InListContext(PredicateContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterInList(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitInList(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitInList(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class NullPredicateContext extends PredicateContext {
		public TerminalNode IS() { return getToken(SqlBaseParser.IS, 0); }
		public TerminalNode NULL() { return getToken(SqlBaseParser.NULL, 0); }
		public TerminalNode NOT() { return getToken(SqlBaseParser.NOT, 0); }
		public NullPredicateContext(PredicateContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterNullPredicate(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitNullPredicate(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitNullPredicate(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class PosixComparisonContext extends PredicateContext {
		public ValueExpressionContext pattern;
		public ValueExpressionContext valueExpression() {
			return getRuleContext(ValueExpressionContext.class,0);
		}
		public TerminalNode REGEX_MATCH() { return getToken(SqlBaseParser.REGEX_MATCH, 0); }
		public QuotedRegexMatchContext quotedRegexMatch() {
			return getRuleContext(QuotedRegexMatchContext.class,0);
		}
		public TerminalNode NOT() { return getToken(SqlBaseParser.NOT, 0); }
		public TerminalNode ASTERISK() { return getToken(SqlBaseParser.ASTERISK, 0); }
		public PosixComparisonContext(PredicateContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterPosixComparison(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitPosixComparison(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitPosixComparison(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class BetweenContext extends PredicateContext {
		public ValueExpressionContext lower;
		public ValueExpressionContext upper;
		public TerminalNode BETWEEN() { return getToken(SqlBaseParser.BETWEEN, 0); }
		public TerminalNode AND() { return getToken(SqlBaseParser.AND, 0); }
		public List<ValueExpressionContext> valueExpression() {
			return getRuleContexts(ValueExpressionContext.class);
		}
		public ValueExpressionContext valueExpression(int i) {
			return getRuleContext(ValueExpressionContext.class,i);
		}
		public TerminalNode NOT() { return getToken(SqlBaseParser.NOT, 0); }
		public BetweenContext(PredicateContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterBetween(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitBetween(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitBetween(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class QuantifiedComparisonContext extends PredicateContext {
		public ComparisonOperatorContext comparisonOperator() {
			return getRuleContext(ComparisonOperatorContext.class,0);
		}
		public ComparisonQuantifierContext comparisonQuantifier() {
			return getRuleContext(ComparisonQuantifierContext.class,0);
		}
		public FunctionExpressionContext functionExpression() {
			return getRuleContext(FunctionExpressionContext.class,0);
		}
		public QueryContext query() {
			return getRuleContext(QueryContext.class,0);
		}
		public QuantifiedComparisonContext(PredicateContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterQuantifiedComparison(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitQuantifiedComparison(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitQuantifiedComparison(this);
			else return visitor.visitChildren(this);
		}
	}

	public final PredicateContext predicate(ParserRuleContext value) throws RecognitionException {
		PredicateContext _localctx = new PredicateContext(_ctx, getState(), value);
		enterRule(_localctx, 100, RULE_predicate);
		int _la;
		try {
			setState(1774);
			_errHandler.sync(this);
			switch ( getInterpreter().adaptivePredict(_input,235,_ctx) ) {
			case 1:
				_localctx = new QuantifiedComparisonContext(_localctx);
				enterOuterAlt(_localctx, 1);
				{
				setState(1686);
				comparisonOperator();
				setState(1687);
				comparisonQuantifier();
				setState(1688);
				match(T__1);
				setState(1689);
				functionExpression();
				setState(1690);
				match(T__2);
				}
				break;
			case 2:
				_localctx = new PosixComparisonContext(_localctx);
				enterOuterAlt(_localctx, 2);
				{
				setState(1693);
				_errHandler.sync(this);
				_la = _input.LA(1);
				if (_la==NOT) {
					{
					setState(1692);
					match(NOT);
					}
				}

				setState(1697);
				_errHandler.sync(this);
				switch (_input.LA(1)) {
				case REGEX_MATCH:
					{
					setState(1695);
					match(REGEX_MATCH);
					}
					break;
				case OPERATOR:
					{
					setState(1696);
					quotedRegexMatch();
					}
					break;
				default:
					throw new NoViableAltException(this);
				}
				setState(1700);
				_errHandler.sync(this);
				_la = _input.LA(1);
				if (_la==ASTERISK) {
					{
					setState(1699);
					match(ASTERISK);
					}
				}

				setState(1702);
				((PosixComparisonContext)_localctx).pattern = valueExpression(0);
				}
				break;
			case 3:
				_localctx = new ComparisonContext(_localctx);
				enterOuterAlt(_localctx, 3);
				{
				setState(1703);
				match(OPERATOR);
				setState(1704);
				match(T__1);
				setState(1707);
				_errHandler.sync(this);
				_la = _input.LA(1);
				if (_la==IDENTIFIER) {
					{
					setState(1705);
					match(IDENTIFIER);
					setState(1706);
					match(T__0);
					}
				}

				setState(1709);
				comparisonOperator();
				setState(1710);
				match(T__2);
				setState(1711);
				((ComparisonContext)_localctx).right = valueExpression(0);
				}
				break;
			case 4:
				_localctx = new ComparisonContext(_localctx);
				enterOuterAlt(_localctx, 4);
				{
				setState(1713);
				comparisonOperator();
				setState(1714);
				((ComparisonContext)_localctx).right = valueExpression(0);
				}
				break;
			case 5:
				_localctx = new QuantifiedComparisonContext(_localctx);
				enterOuterAlt(_localctx, 5);
				{
				setState(1716);
				comparisonOperator();
				setState(1717);
				comparisonQuantifier();
				setState(1718);
				match(T__1);
				setState(1719);
				query();
				setState(1720);
				match(T__2);
				}
				break;
			case 6:
				_localctx = new BetweenContext(_localctx);
				enterOuterAlt(_localctx, 6);
				{
				setState(1723);
				_errHandler.sync(this);
				_la = _input.LA(1);
				if (_la==NOT) {
					{
					setState(1722);
					match(NOT);
					}
				}

				setState(1725);
				match(BETWEEN);
				setState(1726);
				((BetweenContext)_localctx).lower = valueExpression(0);
				setState(1727);
				match(AND);
				setState(1728);
				((BetweenContext)_localctx).upper = valueExpression(0);
				}
				break;
			case 7:
				_localctx = new InListContext(_localctx);
				enterOuterAlt(_localctx, 7);
				{
				setState(1731);
				_errHandler.sync(this);
				_la = _input.LA(1);
				if (_la==NOT) {
					{
					setState(1730);
					match(NOT);
					}
				}

				setState(1733);
				match(IN);
				setState(1734);
				match(T__1);
				setState(1735);
				expression();
				setState(1740);
				_errHandler.sync(this);
				_la = _input.LA(1);
				while (_la==T__3) {
					{
					{
					setState(1736);
					match(T__3);
					setState(1737);
					expression();
					}
					}
					setState(1742);
					_errHandler.sync(this);
					_la = _input.LA(1);
				}
				setState(1743);
				match(T__2);
				}
				break;
			case 8:
				_localctx = new InSubqueryContext(_localctx);
				enterOuterAlt(_localctx, 8);
				{
				setState(1746);
				_errHandler.sync(this);
				_la = _input.LA(1);
				if (_la==NOT) {
					{
					setState(1745);
					match(NOT);
					}
				}

				setState(1748);
				match(IN);
				setState(1749);
				match(T__1);
				setState(1750);
				query();
				setState(1751);
				match(T__2);
				}
				break;
			case 9:
				_localctx = new LikeContext(_localctx);
				enterOuterAlt(_localctx, 9);
				{
				setState(1754);
				_errHandler.sync(this);
				_la = _input.LA(1);
				if (_la==NOT) {
					{
					setState(1753);
					match(NOT);
					}
				}

				setState(1756);
				match(LIKE);
				setState(1757);
				((LikeContext)_localctx).pattern = valueExpression(0);
				setState(1760);
				_errHandler.sync(this);
				switch ( getInterpreter().adaptivePredict(_input,232,_ctx) ) {
				case 1:
					{
					setState(1758);
					match(ESCAPE);
					setState(1759);
					((LikeContext)_localctx).escape = valueExpression(0);
					}
					break;
				}
				}
				break;
			case 10:
				_localctx = new NullPredicateContext(_localctx);
				enterOuterAlt(_localctx, 10);
				{
				setState(1762);
				match(IS);
				setState(1764);
				_errHandler.sync(this);
				_la = _input.LA(1);
				if (_la==NOT) {
					{
					setState(1763);
					match(NOT);
					}
				}

				setState(1766);
				match(NULL);
				}
				break;
			case 11:
				_localctx = new DistinctFromContext(_localctx);
				enterOuterAlt(_localctx, 11);
				{
				setState(1767);
				match(IS);
				setState(1769);
				_errHandler.sync(this);
				_la = _input.LA(1);
				if (_la==NOT) {
					{
					setState(1768);
					match(NOT);
					}
				}

				setState(1771);
				match(DISTINCT);
				setState(1772);
				match(FROM);
				setState(1773);
				((DistinctFromContext)_localctx).right = valueExpression(0);
				}
				break;
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
	public static class FunctionExpressionContext extends ParserRuleContext {
		public QualifiedNameContext qualifiedName() {
			return getRuleContext(QualifiedNameContext.class,0);
		}
		public List<ExpressionContext> expression() {
			return getRuleContexts(ExpressionContext.class);
		}
		public ExpressionContext expression(int i) {
			return getRuleContext(ExpressionContext.class,i);
		}
		public FunctionExpressionContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_functionExpression; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterFunctionExpression(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitFunctionExpression(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitFunctionExpression(this);
			else return visitor.visitChildren(this);
		}
	}

	public final FunctionExpressionContext functionExpression() throws RecognitionException {
		FunctionExpressionContext _localctx = new FunctionExpressionContext(_ctx, getState());
		enterRule(_localctx, 102, RULE_functionExpression);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(1776);
			qualifiedName();
			setState(1777);
			match(T__1);
			setState(1778);
			expression();
			setState(1783);
			_errHandler.sync(this);
			_la = _input.LA(1);
			while (_la==T__3) {
				{
				{
				setState(1779);
				match(T__3);
				setState(1780);
				expression();
				}
				}
				setState(1785);
				_errHandler.sync(this);
				_la = _input.LA(1);
			}
			setState(1786);
			match(T__2);
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
	public static class ValueExpressionContext extends ParserRuleContext {
		public ValueExpressionContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_valueExpression; }
	 
		public ValueExpressionContext() { }
		public void copyFrom(ValueExpressionContext ctx) {
			super.copyFrom(ctx);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class ValueExpressionDefaultContext extends ValueExpressionContext {
		public PrimaryExpressionContext primaryExpression() {
			return getRuleContext(PrimaryExpressionContext.class,0);
		}
		public CollateClauseContext collateClause() {
			return getRuleContext(CollateClauseContext.class,0);
		}
		public ValueExpressionDefaultContext(ValueExpressionContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterValueExpressionDefault(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitValueExpressionDefault(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitValueExpressionDefault(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class ConcatenationContext extends ValueExpressionContext {
		public ValueExpressionContext left;
		public ValueExpressionContext right;
		public TerminalNode CONCAT() { return getToken(SqlBaseParser.CONCAT, 0); }
		public List<ValueExpressionContext> valueExpression() {
			return getRuleContexts(ValueExpressionContext.class);
		}
		public ValueExpressionContext valueExpression(int i) {
			return getRuleContext(ValueExpressionContext.class,i);
		}
		public ConcatenationContext(ValueExpressionContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterConcatenation(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitConcatenation(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitConcatenation(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class ArithmeticBinaryContext extends ValueExpressionContext {
		public ValueExpressionContext left;
		public Token operator;
		public ValueExpressionContext right;
		public List<ValueExpressionContext> valueExpression() {
			return getRuleContexts(ValueExpressionContext.class);
		}
		public ValueExpressionContext valueExpression(int i) {
			return getRuleContext(ValueExpressionContext.class,i);
		}
		public TerminalNode ASTERISK() { return getToken(SqlBaseParser.ASTERISK, 0); }
		public TerminalNode SLASH() { return getToken(SqlBaseParser.SLASH, 0); }
		public TerminalNode PERCENT() { return getToken(SqlBaseParser.PERCENT, 0); }
		public TerminalNode PLUS() { return getToken(SqlBaseParser.PLUS, 0); }
		public TerminalNode MINUS() { return getToken(SqlBaseParser.MINUS, 0); }
		public TerminalNode OPERATOR() { return getToken(SqlBaseParser.OPERATOR, 0); }
		public TerminalNode IDENTIFIER() { return getToken(SqlBaseParser.IDENTIFIER, 0); }
		public ArithmeticBinaryContext(ValueExpressionContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterArithmeticBinary(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitArithmeticBinary(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitArithmeticBinary(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class ArithmeticUnaryContext extends ValueExpressionContext {
		public Token operator;
		public ValueExpressionContext valueExpression() {
			return getRuleContext(ValueExpressionContext.class,0);
		}
		public TerminalNode MINUS() { return getToken(SqlBaseParser.MINUS, 0); }
		public TerminalNode PLUS() { return getToken(SqlBaseParser.PLUS, 0); }
		public ArithmeticUnaryContext(ValueExpressionContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterArithmeticUnary(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitArithmeticUnary(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitArithmeticUnary(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class AtTimeZoneContext extends ValueExpressionContext {
		public ValueExpressionContext valueExpression() {
			return getRuleContext(ValueExpressionContext.class,0);
		}
		public TerminalNode AT() { return getToken(SqlBaseParser.AT, 0); }
		public TimeZoneSpecifierContext timeZoneSpecifier() {
			return getRuleContext(TimeZoneSpecifierContext.class,0);
		}
		public AtTimeZoneContext(ValueExpressionContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterAtTimeZone(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitAtTimeZone(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitAtTimeZone(this);
			else return visitor.visitChildren(this);
		}
	}

	public final ValueExpressionContext valueExpression() throws RecognitionException {
		return valueExpression(0);
	}

	private ValueExpressionContext valueExpression(int _p) throws RecognitionException {
		ParserRuleContext _parentctx = _ctx;
		int _parentState = getState();
		ValueExpressionContext _localctx = new ValueExpressionContext(_ctx, _parentState);
		ValueExpressionContext _prevctx = _localctx;
		int _startState = 104;
		enterRecursionRule(_localctx, 104, RULE_valueExpression, _p);
		int _la;
		try {
			int _alt;
			enterOuterAlt(_localctx, 1);
			{
			setState(1796);
			_errHandler.sync(this);
			switch ( getInterpreter().adaptivePredict(_input,238,_ctx) ) {
			case 1:
				{
				_localctx = new ValueExpressionDefaultContext(_localctx);
				_ctx = _localctx;
				_prevctx = _localctx;

				setState(1789);
				primaryExpression(0);
				setState(1791);
				_errHandler.sync(this);
				switch ( getInterpreter().adaptivePredict(_input,237,_ctx) ) {
				case 1:
					{
					setState(1790);
					collateClause();
					}
					break;
				}
				}
				break;
			case 2:
				{
				_localctx = new ValueExpressionDefaultContext(_localctx);
				_ctx = _localctx;
				_prevctx = _localctx;
				setState(1793);
				primaryExpression(0);
				}
				break;
			case 3:
				{
				_localctx = new ArithmeticUnaryContext(_localctx);
				_ctx = _localctx;
				_prevctx = _localctx;
				setState(1794);
				((ArithmeticUnaryContext)_localctx).operator = _input.LT(1);
				_la = _input.LA(1);
				if ( !(_la==PLUS || _la==MINUS) ) {
					((ArithmeticUnaryContext)_localctx).operator = (Token)_errHandler.recoverInline(this);
				}
				else {
					if ( _input.LA(1)==Token.EOF ) matchedEOF = true;
					_errHandler.reportMatch(this);
					consume();
				}
				setState(1795);
				valueExpression(5);
				}
				break;
			}
			_ctx.stop = _input.LT(-1);
			setState(1822);
			_errHandler.sync(this);
			_alt = getInterpreter().adaptivePredict(_input,241,_ctx);
			while ( _alt!=2 && _alt!=org.antlr.v4.runtime.atn.ATN.INVALID_ALT_NUMBER ) {
				if ( _alt==1 ) {
					if ( _parseListeners!=null ) triggerExitRuleEvent();
					_prevctx = _localctx;
					{
					setState(1820);
					_errHandler.sync(this);
					switch ( getInterpreter().adaptivePredict(_input,240,_ctx) ) {
					case 1:
						{
						_localctx = new ArithmeticBinaryContext(new ValueExpressionContext(_parentctx, _parentState));
						((ArithmeticBinaryContext)_localctx).left = _prevctx;
						pushNewRecursionContext(_localctx, _startState, RULE_valueExpression);
						setState(1798);
						if (!(precpred(_ctx, 4))) throw new FailedPredicateException(this, "precpred(_ctx, 4)");
						setState(1799);
						((ArithmeticBinaryContext)_localctx).operator = _input.LT(1);
						_la = _input.LA(1);
						if ( !(((((_la - 276)) & ~0x3f) == 0 && ((1L << (_la - 276)) & 7L) != 0)) ) {
							((ArithmeticBinaryContext)_localctx).operator = (Token)_errHandler.recoverInline(this);
						}
						else {
							if ( _input.LA(1)==Token.EOF ) matchedEOF = true;
							_errHandler.reportMatch(this);
							consume();
						}
						setState(1800);
						((ArithmeticBinaryContext)_localctx).right = valueExpression(5);
						}
						break;
					case 2:
						{
						_localctx = new ArithmeticBinaryContext(new ValueExpressionContext(_parentctx, _parentState));
						((ArithmeticBinaryContext)_localctx).left = _prevctx;
						pushNewRecursionContext(_localctx, _startState, RULE_valueExpression);
						setState(1801);
						if (!(precpred(_ctx, 3))) throw new FailedPredicateException(this, "precpred(_ctx, 3)");
						setState(1802);
						((ArithmeticBinaryContext)_localctx).operator = _input.LT(1);
						_la = _input.LA(1);
						if ( !(_la==PLUS || _la==MINUS) ) {
							((ArithmeticBinaryContext)_localctx).operator = (Token)_errHandler.recoverInline(this);
						}
						else {
							if ( _input.LA(1)==Token.EOF ) matchedEOF = true;
							_errHandler.reportMatch(this);
							consume();
						}
						setState(1803);
						((ArithmeticBinaryContext)_localctx).right = valueExpression(4);
						}
						break;
					case 3:
						{
						_localctx = new ArithmeticBinaryContext(new ValueExpressionContext(_parentctx, _parentState));
						((ArithmeticBinaryContext)_localctx).left = _prevctx;
						pushNewRecursionContext(_localctx, _startState, RULE_valueExpression);
						setState(1804);
						if (!(precpred(_ctx, 2))) throw new FailedPredicateException(this, "precpred(_ctx, 2)");
						setState(1805);
						match(OPERATOR);
						setState(1806);
						match(T__1);
						setState(1809);
						_errHandler.sync(this);
						_la = _input.LA(1);
						if (_la==IDENTIFIER) {
							{
							setState(1807);
							match(IDENTIFIER);
							setState(1808);
							match(T__0);
							}
						}

						setState(1811);
						((ArithmeticBinaryContext)_localctx).operator = _input.LT(1);
						_la = _input.LA(1);
						if ( !(((((_la - 274)) & ~0x3f) == 0 && ((1L << (_la - 274)) & 31L) != 0)) ) {
							((ArithmeticBinaryContext)_localctx).operator = (Token)_errHandler.recoverInline(this);
						}
						else {
							if ( _input.LA(1)==Token.EOF ) matchedEOF = true;
							_errHandler.reportMatch(this);
							consume();
						}
						setState(1812);
						match(T__2);
						setState(1813);
						((ArithmeticBinaryContext)_localctx).right = valueExpression(3);
						}
						break;
					case 4:
						{
						_localctx = new ConcatenationContext(new ValueExpressionContext(_parentctx, _parentState));
						((ConcatenationContext)_localctx).left = _prevctx;
						pushNewRecursionContext(_localctx, _startState, RULE_valueExpression);
						setState(1814);
						if (!(precpred(_ctx, 1))) throw new FailedPredicateException(this, "precpred(_ctx, 1)");
						setState(1815);
						match(CONCAT);
						setState(1816);
						((ConcatenationContext)_localctx).right = valueExpression(2);
						}
						break;
					case 5:
						{
						_localctx = new AtTimeZoneContext(new ValueExpressionContext(_parentctx, _parentState));
						pushNewRecursionContext(_localctx, _startState, RULE_valueExpression);
						setState(1817);
						if (!(precpred(_ctx, 6))) throw new FailedPredicateException(this, "precpred(_ctx, 6)");
						setState(1818);
						match(AT);
						setState(1819);
						timeZoneSpecifier();
						}
						break;
					}
					} 
				}
				setState(1824);
				_errHandler.sync(this);
				_alt = getInterpreter().adaptivePredict(_input,241,_ctx);
			}
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			unrollRecursionContexts(_parentctx);
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class PrimaryExpressionContext extends ParserRuleContext {
		public PrimaryExpressionContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_primaryExpression; }
	 
		public PrimaryExpressionContext() { }
		public void copyFrom(PrimaryExpressionContext ctx) {
			super.copyFrom(ctx);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class DereferenceContext extends PrimaryExpressionContext {
		public PrimaryExpressionContext base;
		public IdentifierContext fieldName;
		public PrimaryExpressionContext primaryExpression() {
			return getRuleContext(PrimaryExpressionContext.class,0);
		}
		public IdentifierContext identifier() {
			return getRuleContext(IdentifierContext.class,0);
		}
		public DereferenceContext(PrimaryExpressionContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterDereference(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitDereference(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitDereference(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class TypeConstructorContext extends PrimaryExpressionContext {
		public IdentifierContext identifier() {
			return getRuleContext(IdentifierContext.class,0);
		}
		public StringContext string() {
			return getRuleContext(StringContext.class,0);
		}
		public TerminalNode DOUBLE() { return getToken(SqlBaseParser.DOUBLE, 0); }
		public TerminalNode PRECISION() { return getToken(SqlBaseParser.PRECISION, 0); }
		public TerminalNode PG_CAST() { return getToken(SqlBaseParser.PG_CAST, 0); }
		public TerminalNode IDENTIFIER() { return getToken(SqlBaseParser.IDENTIFIER, 0); }
		public TypeConstructorContext(PrimaryExpressionContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterTypeConstructor(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitTypeConstructor(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitTypeConstructor(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class SpecialDateTimeFunctionContext extends PrimaryExpressionContext {
		public Token name;
		public Token precision;
		public TerminalNode CURRENT_DATE() { return getToken(SqlBaseParser.CURRENT_DATE, 0); }
		public TerminalNode CURRENT_TIME() { return getToken(SqlBaseParser.CURRENT_TIME, 0); }
		public TerminalNode INTEGER_VALUE() { return getToken(SqlBaseParser.INTEGER_VALUE, 0); }
		public TerminalNode CURRENT_TIMESTAMP() { return getToken(SqlBaseParser.CURRENT_TIMESTAMP, 0); }
		public TerminalNode LOCALTIME() { return getToken(SqlBaseParser.LOCALTIME, 0); }
		public TerminalNode LOCALTIMESTAMP() { return getToken(SqlBaseParser.LOCALTIMESTAMP, 0); }
		public SpecialDateTimeFunctionContext(PrimaryExpressionContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterSpecialDateTimeFunction(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitSpecialDateTimeFunction(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitSpecialDateTimeFunction(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class SubstringContext extends PrimaryExpressionContext {
		public TerminalNode SUBSTRING() { return getToken(SqlBaseParser.SUBSTRING, 0); }
		public List<ValueExpressionContext> valueExpression() {
			return getRuleContexts(ValueExpressionContext.class);
		}
		public ValueExpressionContext valueExpression(int i) {
			return getRuleContext(ValueExpressionContext.class,i);
		}
		public TerminalNode FROM() { return getToken(SqlBaseParser.FROM, 0); }
		public TerminalNode FOR() { return getToken(SqlBaseParser.FOR, 0); }
		public SubstringContext(PrimaryExpressionContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterSubstring(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitSubstring(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitSubstring(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class CastContext extends PrimaryExpressionContext {
		public TerminalNode CAST() { return getToken(SqlBaseParser.CAST, 0); }
		public ExpressionContext expression() {
			return getRuleContext(ExpressionContext.class,0);
		}
		public TerminalNode AS() { return getToken(SqlBaseParser.AS, 0); }
		public TypeContext type() {
			return getRuleContext(TypeContext.class,0);
		}
		public TerminalNode TRY_CAST() { return getToken(SqlBaseParser.TRY_CAST, 0); }
		public TerminalNode IDENTIFIER() { return getToken(SqlBaseParser.IDENTIFIER, 0); }
		public PrimaryExpressionContext primaryExpression() {
			return getRuleContext(PrimaryExpressionContext.class,0);
		}
		public TerminalNode PG_CAST() { return getToken(SqlBaseParser.PG_CAST, 0); }
		public CastContext(PrimaryExpressionContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterCast(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitCast(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitCast(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class LambdaContext extends PrimaryExpressionContext {
		public List<IdentifierContext> identifier() {
			return getRuleContexts(IdentifierContext.class);
		}
		public IdentifierContext identifier(int i) {
			return getRuleContext(IdentifierContext.class,i);
		}
		public ExpressionContext expression() {
			return getRuleContext(ExpressionContext.class,0);
		}
		public LambdaContext(PrimaryExpressionContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterLambda(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitLambda(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitLambda(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class ParenthesizedExpressionContext extends PrimaryExpressionContext {
		public ExpressionContext expression() {
			return getRuleContext(ExpressionContext.class,0);
		}
		public ParenthesizedExpressionContext(PrimaryExpressionContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterParenthesizedExpression(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitParenthesizedExpression(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitParenthesizedExpression(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class ParameterContext extends PrimaryExpressionContext {
		public TerminalNode QUESTION_MARK() { return getToken(SqlBaseParser.QUESTION_MARK, 0); }
		public ParameterContext(PrimaryExpressionContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterParameter(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitParameter(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitParameter(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class NormalizeContext extends PrimaryExpressionContext {
		public TerminalNode NORMALIZE() { return getToken(SqlBaseParser.NORMALIZE, 0); }
		public ValueExpressionContext valueExpression() {
			return getRuleContext(ValueExpressionContext.class,0);
		}
		public NormalFormContext normalForm() {
			return getRuleContext(NormalFormContext.class,0);
		}
		public NormalizeContext(PrimaryExpressionContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterNormalize(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitNormalize(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitNormalize(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class IntervalLiteralContext extends PrimaryExpressionContext {
		public IntervalContext interval() {
			return getRuleContext(IntervalContext.class,0);
		}
		public IntervalLiteralContext(PrimaryExpressionContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterIntervalLiteral(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitIntervalLiteral(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitIntervalLiteral(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class NumericLiteralContext extends PrimaryExpressionContext {
		public NumberContext number() {
			return getRuleContext(NumberContext.class,0);
		}
		public NumericLiteralContext(PrimaryExpressionContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterNumericLiteral(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitNumericLiteral(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitNumericLiteral(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class BooleanLiteralContext extends PrimaryExpressionContext {
		public BooleanValueContext booleanValue() {
			return getRuleContext(BooleanValueContext.class,0);
		}
		public BooleanLiteralContext(PrimaryExpressionContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterBooleanLiteral(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitBooleanLiteral(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitBooleanLiteral(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class SimpleCaseContext extends PrimaryExpressionContext {
		public ExpressionContext operand;
		public ExpressionContext elseExpression;
		public TerminalNode CASE() { return getToken(SqlBaseParser.CASE, 0); }
		public TerminalNode END() { return getToken(SqlBaseParser.END, 0); }
		public List<ExpressionContext> expression() {
			return getRuleContexts(ExpressionContext.class);
		}
		public ExpressionContext expression(int i) {
			return getRuleContext(ExpressionContext.class,i);
		}
		public List<WhenClauseContext> whenClause() {
			return getRuleContexts(WhenClauseContext.class);
		}
		public WhenClauseContext whenClause(int i) {
			return getRuleContext(WhenClauseContext.class,i);
		}
		public TerminalNode ELSE() { return getToken(SqlBaseParser.ELSE, 0); }
		public SimpleCaseContext(PrimaryExpressionContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterSimpleCase(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitSimpleCase(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitSimpleCase(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class ColumnReferenceContext extends PrimaryExpressionContext {
		public IdentifierContext identifier() {
			return getRuleContext(IdentifierContext.class,0);
		}
		public ColumnReferenceContext(PrimaryExpressionContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterColumnReference(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitColumnReference(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitColumnReference(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class NullLiteralContext extends PrimaryExpressionContext {
		public TerminalNode NULL() { return getToken(SqlBaseParser.NULL, 0); }
		public NullLiteralContext(PrimaryExpressionContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterNullLiteral(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitNullLiteral(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitNullLiteral(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class RowConstructorContext extends PrimaryExpressionContext {
		public List<ExpressionContext> expression() {
			return getRuleContexts(ExpressionContext.class);
		}
		public ExpressionContext expression(int i) {
			return getRuleContext(ExpressionContext.class,i);
		}
		public TerminalNode ROW() { return getToken(SqlBaseParser.ROW, 0); }
		public RowConstructorContext(PrimaryExpressionContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterRowConstructor(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitRowConstructor(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitRowConstructor(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class SubscriptContext extends PrimaryExpressionContext {
		public PrimaryExpressionContext value;
		public ValueExpressionContext index;
		public PrimaryExpressionContext primaryExpression() {
			return getRuleContext(PrimaryExpressionContext.class,0);
		}
		public ValueExpressionContext valueExpression() {
			return getRuleContext(ValueExpressionContext.class,0);
		}
		public SubscriptContext(PrimaryExpressionContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterSubscript(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitSubscript(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitSubscript(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class CurrentPathContext extends PrimaryExpressionContext {
		public Token name;
		public TerminalNode CURRENT_PATH() { return getToken(SqlBaseParser.CURRENT_PATH, 0); }
		public CurrentPathContext(PrimaryExpressionContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterCurrentPath(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitCurrentPath(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitCurrentPath(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class SubqueryExpressionContext extends PrimaryExpressionContext {
		public QueryContext query() {
			return getRuleContext(QueryContext.class,0);
		}
		public SubqueryExpressionContext(PrimaryExpressionContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterSubqueryExpression(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitSubqueryExpression(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitSubqueryExpression(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class BinaryLiteralContext extends PrimaryExpressionContext {
		public TerminalNode BINARY_LITERAL() { return getToken(SqlBaseParser.BINARY_LITERAL, 0); }
		public BinaryLiteralContext(PrimaryExpressionContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterBinaryLiteral(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitBinaryLiteral(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitBinaryLiteral(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class CurrentUserContext extends PrimaryExpressionContext {
		public Token name;
		public TerminalNode CURRENT_USER() { return getToken(SqlBaseParser.CURRENT_USER, 0); }
		public CurrentUserContext(PrimaryExpressionContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterCurrentUser(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitCurrentUser(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitCurrentUser(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class MeasureContext extends PrimaryExpressionContext {
		public IdentifierContext identifier() {
			return getRuleContext(IdentifierContext.class,0);
		}
		public OverContext over() {
			return getRuleContext(OverContext.class,0);
		}
		public MeasureContext(PrimaryExpressionContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterMeasure(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitMeasure(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitMeasure(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class ExtractContext extends PrimaryExpressionContext {
		public TerminalNode EXTRACT() { return getToken(SqlBaseParser.EXTRACT, 0); }
		public IdentifierContext identifier() {
			return getRuleContext(IdentifierContext.class,0);
		}
		public TerminalNode FROM() { return getToken(SqlBaseParser.FROM, 0); }
		public ValueExpressionContext valueExpression() {
			return getRuleContext(ValueExpressionContext.class,0);
		}
		public ExtractContext(PrimaryExpressionContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterExtract(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitExtract(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitExtract(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class StringLiteralContext extends PrimaryExpressionContext {
		public StringContext string() {
			return getRuleContext(StringContext.class,0);
		}
		public StringLiteralContext(PrimaryExpressionContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterStringLiteral(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitStringLiteral(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitStringLiteral(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class ArrayConstructorContext extends PrimaryExpressionContext {
		public TerminalNode ARRAY() { return getToken(SqlBaseParser.ARRAY, 0); }
		public List<ExpressionContext> expression() {
			return getRuleContexts(ExpressionContext.class);
		}
		public ExpressionContext expression(int i) {
			return getRuleContext(ExpressionContext.class,i);
		}
		public ArrayConstructorContext(PrimaryExpressionContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterArrayConstructor(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitArrayConstructor(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitArrayConstructor(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class FunctionCallContext extends PrimaryExpressionContext {
		public IdentifierContext label;
		public QualifiedNameContext qualifiedName() {
			return getRuleContext(QualifiedNameContext.class,0);
		}
		public TerminalNode ASTERISK() { return getToken(SqlBaseParser.ASTERISK, 0); }
		public ProcessingModeContext processingMode() {
			return getRuleContext(ProcessingModeContext.class,0);
		}
		public FilterContext filter() {
			return getRuleContext(FilterContext.class,0);
		}
		public OverContext over() {
			return getRuleContext(OverContext.class,0);
		}
		public IdentifierContext identifier() {
			return getRuleContext(IdentifierContext.class,0);
		}
		public List<ExpressionContext> expression() {
			return getRuleContexts(ExpressionContext.class);
		}
		public ExpressionContext expression(int i) {
			return getRuleContext(ExpressionContext.class,i);
		}
		public TerminalNode ORDER() { return getToken(SqlBaseParser.ORDER, 0); }
		public TerminalNode BY() { return getToken(SqlBaseParser.BY, 0); }
		public List<SortItemContext> sortItem() {
			return getRuleContexts(SortItemContext.class);
		}
		public SortItemContext sortItem(int i) {
			return getRuleContext(SortItemContext.class,i);
		}
		public SetQuantifierContext setQuantifier() {
			return getRuleContext(SetQuantifierContext.class,0);
		}
		public NullTreatmentContext nullTreatment() {
			return getRuleContext(NullTreatmentContext.class,0);
		}
		public FunctionCallContext(PrimaryExpressionContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterFunctionCall(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitFunctionCall(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitFunctionCall(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class CurrentSchemaContext extends PrimaryExpressionContext {
		public Token name;
		public TerminalNode CURRENT_SCHEMA() { return getToken(SqlBaseParser.CURRENT_SCHEMA, 0); }
		public IdentifierContext identifier() {
			return getRuleContext(IdentifierContext.class,0);
		}
		public CurrentSchemaContext(PrimaryExpressionContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterCurrentSchema(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitCurrentSchema(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitCurrentSchema(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class ExistsContext extends PrimaryExpressionContext {
		public TerminalNode EXISTS() { return getToken(SqlBaseParser.EXISTS, 0); }
		public QueryContext query() {
			return getRuleContext(QueryContext.class,0);
		}
		public ExistsContext(PrimaryExpressionContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterExists(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitExists(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitExists(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class PositionContext extends PrimaryExpressionContext {
		public TerminalNode POSITION() { return getToken(SqlBaseParser.POSITION, 0); }
		public List<ValueExpressionContext> valueExpression() {
			return getRuleContexts(ValueExpressionContext.class);
		}
		public ValueExpressionContext valueExpression(int i) {
			return getRuleContext(ValueExpressionContext.class,i);
		}
		public TerminalNode IN() { return getToken(SqlBaseParser.IN, 0); }
		public PositionContext(PrimaryExpressionContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterPosition(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitPosition(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitPosition(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class ListaggContext extends PrimaryExpressionContext {
		public Token name;
		public ExpressionContext expression() {
			return getRuleContext(ExpressionContext.class,0);
		}
		public TerminalNode LISTAGG() { return getToken(SqlBaseParser.LISTAGG, 0); }
		public TerminalNode WITHIN() { return getToken(SqlBaseParser.WITHIN, 0); }
		public TerminalNode GROUP() { return getToken(SqlBaseParser.GROUP, 0); }
		public TerminalNode ORDER() { return getToken(SqlBaseParser.ORDER, 0); }
		public TerminalNode BY() { return getToken(SqlBaseParser.BY, 0); }
		public List<SortItemContext> sortItem() {
			return getRuleContexts(SortItemContext.class);
		}
		public SortItemContext sortItem(int i) {
			return getRuleContext(SortItemContext.class,i);
		}
		public SetQuantifierContext setQuantifier() {
			return getRuleContext(SetQuantifierContext.class,0);
		}
		public StringContext string() {
			return getRuleContext(StringContext.class,0);
		}
		public TerminalNode ON() { return getToken(SqlBaseParser.ON, 0); }
		public TerminalNode OVERFLOW() { return getToken(SqlBaseParser.OVERFLOW, 0); }
		public ListAggOverflowBehaviorContext listAggOverflowBehavior() {
			return getRuleContext(ListAggOverflowBehaviorContext.class,0);
		}
		public ListaggContext(PrimaryExpressionContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterListagg(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitListagg(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitListagg(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class SearchedCaseContext extends PrimaryExpressionContext {
		public ExpressionContext elseExpression;
		public TerminalNode CASE() { return getToken(SqlBaseParser.CASE, 0); }
		public TerminalNode END() { return getToken(SqlBaseParser.END, 0); }
		public List<WhenClauseContext> whenClause() {
			return getRuleContexts(WhenClauseContext.class);
		}
		public WhenClauseContext whenClause(int i) {
			return getRuleContext(WhenClauseContext.class,i);
		}
		public TerminalNode ELSE() { return getToken(SqlBaseParser.ELSE, 0); }
		public ExpressionContext expression() {
			return getRuleContext(ExpressionContext.class,0);
		}
		public SearchedCaseContext(PrimaryExpressionContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterSearchedCase(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitSearchedCase(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitSearchedCase(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class CurrentCatalogContext extends PrimaryExpressionContext {
		public Token name;
		public TerminalNode CURRENT_CATALOG() { return getToken(SqlBaseParser.CURRENT_CATALOG, 0); }
		public CurrentCatalogContext(PrimaryExpressionContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterCurrentCatalog(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitCurrentCatalog(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitCurrentCatalog(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class GroupingOperationContext extends PrimaryExpressionContext {
		public TerminalNode GROUPING() { return getToken(SqlBaseParser.GROUPING, 0); }
		public List<QualifiedNameContext> qualifiedName() {
			return getRuleContexts(QualifiedNameContext.class);
		}
		public QualifiedNameContext qualifiedName(int i) {
			return getRuleContext(QualifiedNameContext.class,i);
		}
		public GroupingOperationContext(PrimaryExpressionContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterGroupingOperation(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitGroupingOperation(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitGroupingOperation(this);
			else return visitor.visitChildren(this);
		}
	}

	public final PrimaryExpressionContext primaryExpression() throws RecognitionException {
		return primaryExpression(0);
	}

	private PrimaryExpressionContext primaryExpression(int _p) throws RecognitionException {
		ParserRuleContext _parentctx = _ctx;
		int _parentState = getState();
		PrimaryExpressionContext _localctx = new PrimaryExpressionContext(_ctx, _parentState);
		PrimaryExpressionContext _prevctx = _localctx;
		int _startState = 106;
		enterRecursionRule(_localctx, 106, RULE_primaryExpression, _p);
		int _la;
		try {
			int _alt;
			enterOuterAlt(_localctx, 1);
			{
			setState(2153);
			_errHandler.sync(this);
			switch ( getInterpreter().adaptivePredict(_input,283,_ctx) ) {
			case 1:
				{
				_localctx = new NullLiteralContext(_localctx);
				_ctx = _localctx;
				_prevctx = _localctx;

				setState(1826);
				match(NULL);
				}
				break;
			case 2:
				{
				_localctx = new IntervalLiteralContext(_localctx);
				_ctx = _localctx;
				_prevctx = _localctx;
				setState(1827);
				interval();
				}
				break;
			case 3:
				{
				_localctx = new TypeConstructorContext(_localctx);
				_ctx = _localctx;
				_prevctx = _localctx;
				setState(1828);
				identifier();
				setState(1829);
				string();
				}
				break;
			case 4:
				{
				_localctx = new TypeConstructorContext(_localctx);
				_ctx = _localctx;
				_prevctx = _localctx;
				setState(1831);
				match(DOUBLE);
				setState(1832);
				match(PRECISION);
				setState(1833);
				string();
				}
				break;
			case 5:
				{
				_localctx = new TypeConstructorContext(_localctx);
				_ctx = _localctx;
				_prevctx = _localctx;
				setState(1834);
				string();
				setState(1835);
				match(PG_CAST);
				setState(1838);
				_errHandler.sync(this);
				switch ( getInterpreter().adaptivePredict(_input,242,_ctx) ) {
				case 1:
					{
					setState(1836);
					match(IDENTIFIER);
					setState(1837);
					match(T__0);
					}
					break;
				}
				setState(1840);
				identifier();
				}
				break;
			case 6:
				{
				_localctx = new NumericLiteralContext(_localctx);
				_ctx = _localctx;
				_prevctx = _localctx;
				setState(1842);
				number();
				}
				break;
			case 7:
				{
				_localctx = new BooleanLiteralContext(_localctx);
				_ctx = _localctx;
				_prevctx = _localctx;
				setState(1843);
				booleanValue();
				}
				break;
			case 8:
				{
				_localctx = new StringLiteralContext(_localctx);
				_ctx = _localctx;
				_prevctx = _localctx;
				setState(1844);
				string();
				}
				break;
			case 9:
				{
				_localctx = new BinaryLiteralContext(_localctx);
				_ctx = _localctx;
				_prevctx = _localctx;
				setState(1845);
				match(BINARY_LITERAL);
				}
				break;
			case 10:
				{
				_localctx = new ParameterContext(_localctx);
				_ctx = _localctx;
				_prevctx = _localctx;
				setState(1846);
				match(QUESTION_MARK);
				}
				break;
			case 11:
				{
				_localctx = new PositionContext(_localctx);
				_ctx = _localctx;
				_prevctx = _localctx;
				setState(1847);
				match(POSITION);
				setState(1848);
				match(T__1);
				setState(1849);
				valueExpression(0);
				setState(1850);
				match(IN);
				setState(1851);
				valueExpression(0);
				setState(1852);
				match(T__2);
				}
				break;
			case 12:
				{
				_localctx = new RowConstructorContext(_localctx);
				_ctx = _localctx;
				_prevctx = _localctx;
				setState(1854);
				match(T__1);
				setState(1855);
				expression();
				setState(1858); 
				_errHandler.sync(this);
				_la = _input.LA(1);
				do {
					{
					{
					setState(1856);
					match(T__3);
					setState(1857);
					expression();
					}
					}
					setState(1860); 
					_errHandler.sync(this);
					_la = _input.LA(1);
				} while ( _la==T__3 );
				setState(1862);
				match(T__2);
				}
				break;
			case 13:
				{
				_localctx = new RowConstructorContext(_localctx);
				_ctx = _localctx;
				_prevctx = _localctx;
				setState(1864);
				match(ROW);
				setState(1865);
				match(T__1);
				setState(1866);
				expression();
				setState(1871);
				_errHandler.sync(this);
				_la = _input.LA(1);
				while (_la==T__3) {
					{
					{
					setState(1867);
					match(T__3);
					setState(1868);
					expression();
					}
					}
					setState(1873);
					_errHandler.sync(this);
					_la = _input.LA(1);
				}
				setState(1874);
				match(T__2);
				}
				break;
			case 14:
				{
				_localctx = new ListaggContext(_localctx);
				_ctx = _localctx;
				_prevctx = _localctx;
				setState(1876);
				((ListaggContext)_localctx).name = match(LISTAGG);
				setState(1877);
				match(T__1);
				setState(1879);
				_errHandler.sync(this);
				switch ( getInterpreter().adaptivePredict(_input,245,_ctx) ) {
				case 1:
					{
					setState(1878);
					setQuantifier();
					}
					break;
				}
				setState(1881);
				expression();
				setState(1884);
				_errHandler.sync(this);
				_la = _input.LA(1);
				if (_la==T__3) {
					{
					setState(1882);
					match(T__3);
					setState(1883);
					string();
					}
				}

				setState(1889);
				_errHandler.sync(this);
				_la = _input.LA(1);
				if (_la==ON) {
					{
					setState(1886);
					match(ON);
					setState(1887);
					match(OVERFLOW);
					setState(1888);
					listAggOverflowBehavior();
					}
				}

				setState(1891);
				match(T__2);
				{
				setState(1892);
				match(WITHIN);
				setState(1893);
				match(GROUP);
				setState(1894);
				match(T__1);
				setState(1895);
				match(ORDER);
				setState(1896);
				match(BY);
				setState(1897);
				sortItem();
				setState(1902);
				_errHandler.sync(this);
				_la = _input.LA(1);
				while (_la==T__3) {
					{
					{
					setState(1898);
					match(T__3);
					setState(1899);
					sortItem();
					}
					}
					setState(1904);
					_errHandler.sync(this);
					_la = _input.LA(1);
				}
				setState(1905);
				match(T__2);
				}
				}
				break;
			case 15:
				{
				_localctx = new FunctionCallContext(_localctx);
				_ctx = _localctx;
				_prevctx = _localctx;
				setState(1908);
				_errHandler.sync(this);
				switch ( getInterpreter().adaptivePredict(_input,249,_ctx) ) {
				case 1:
					{
					setState(1907);
					processingMode();
					}
					break;
				}
				setState(1910);
				qualifiedName();
				setState(1911);
				match(T__1);
				setState(1915);
				_errHandler.sync(this);
				_la = _input.LA(1);
				if ((((_la) & ~0x3f) == 0 && ((1L << _la) & -9203672295665565696L) != 0) || ((((_la - 64)) & ~0x3f) == 0 && ((1L << (_la - 64)) & -5424682731988948105L) != 0) || ((((_la - 129)) & ~0x3f) == 0 && ((1L << (_la - 129)) & -1153018544028386985L) != 0) || ((((_la - 193)) & ~0x3f) == 0 && ((1L << (_la - 193)) & -2928537194681353219L) != 0) || ((((_la - 257)) & ~0x3f) == 0 && ((1L << (_la - 257)) & 32212256745L) != 0)) {
					{
					setState(1912);
					((FunctionCallContext)_localctx).label = identifier();
					setState(1913);
					match(T__0);
					}
				}

				setState(1917);
				match(ASTERISK);
				setState(1918);
				match(T__2);
				setState(1920);
				_errHandler.sync(this);
				switch ( getInterpreter().adaptivePredict(_input,251,_ctx) ) {
				case 1:
					{
					setState(1919);
					filter();
					}
					break;
				}
				setState(1923);
				_errHandler.sync(this);
				switch ( getInterpreter().adaptivePredict(_input,252,_ctx) ) {
				case 1:
					{
					setState(1922);
					over();
					}
					break;
				}
				}
				break;
			case 16:
				{
				_localctx = new FunctionCallContext(_localctx);
				_ctx = _localctx;
				_prevctx = _localctx;
				setState(1926);
				_errHandler.sync(this);
				switch ( getInterpreter().adaptivePredict(_input,253,_ctx) ) {
				case 1:
					{
					setState(1925);
					processingMode();
					}
					break;
				}
				setState(1928);
				qualifiedName();
				setState(1929);
				match(T__1);
				setState(1941);
				_errHandler.sync(this);
				_la = _input.LA(1);
				if ((((_la) & ~0x3f) == 0 && ((1L << _la) & -304556133446578172L) != 0) || ((((_la - 64)) & ~0x3f) == 0 && ((1L << (_la - 64)) & -5424665139366691977L) != 0) || ((((_la - 129)) & ~0x3f) == 0 && ((1L << (_la - 129)) & -1153018536512192553L) != 0) || ((((_la - 193)) & ~0x3f) == 0 && ((1L << (_la - 193)) & -2928466825937175555L) != 0) || ((((_la - 257)) & ~0x3f) == 0 && ((1L << (_la - 257)) & 1133846595561L) != 0)) {
					{
					setState(1931);
					_errHandler.sync(this);
					switch ( getInterpreter().adaptivePredict(_input,254,_ctx) ) {
					case 1:
						{
						setState(1930);
						setQuantifier();
						}
						break;
					}
					setState(1933);
					expression();
					setState(1938);
					_errHandler.sync(this);
					_la = _input.LA(1);
					while (_la==T__3) {
						{
						{
						setState(1934);
						match(T__3);
						setState(1935);
						expression();
						}
						}
						setState(1940);
						_errHandler.sync(this);
						_la = _input.LA(1);
					}
					}
				}

				setState(1953);
				_errHandler.sync(this);
				_la = _input.LA(1);
				if (_la==ORDER) {
					{
					setState(1943);
					match(ORDER);
					setState(1944);
					match(BY);
					setState(1945);
					sortItem();
					setState(1950);
					_errHandler.sync(this);
					_la = _input.LA(1);
					while (_la==T__3) {
						{
						{
						setState(1946);
						match(T__3);
						setState(1947);
						sortItem();
						}
						}
						setState(1952);
						_errHandler.sync(this);
						_la = _input.LA(1);
					}
					}
				}

				setState(1955);
				match(T__2);
				setState(1957);
				_errHandler.sync(this);
				switch ( getInterpreter().adaptivePredict(_input,259,_ctx) ) {
				case 1:
					{
					setState(1956);
					filter();
					}
					break;
				}
				setState(1963);
				_errHandler.sync(this);
				switch ( getInterpreter().adaptivePredict(_input,261,_ctx) ) {
				case 1:
					{
					setState(1960);
					_errHandler.sync(this);
					_la = _input.LA(1);
					if (_la==IGNORE || _la==RESPECT) {
						{
						setState(1959);
						nullTreatment();
						}
					}

					setState(1962);
					over();
					}
					break;
				}
				}
				break;
			case 17:
				{
				_localctx = new MeasureContext(_localctx);
				_ctx = _localctx;
				_prevctx = _localctx;
				setState(1965);
				identifier();
				setState(1966);
				over();
				}
				break;
			case 18:
				{
				_localctx = new LambdaContext(_localctx);
				_ctx = _localctx;
				_prevctx = _localctx;
				setState(1968);
				identifier();
				setState(1969);
				match(T__10);
				setState(1970);
				expression();
				}
				break;
			case 19:
				{
				_localctx = new LambdaContext(_localctx);
				_ctx = _localctx;
				_prevctx = _localctx;
				setState(1972);
				match(T__1);
				setState(1981);
				_errHandler.sync(this);
				_la = _input.LA(1);
				if ((((_la) & ~0x3f) == 0 && ((1L << _la) & -9203672295665565696L) != 0) || ((((_la - 64)) & ~0x3f) == 0 && ((1L << (_la - 64)) & -5424682731988948105L) != 0) || ((((_la - 129)) & ~0x3f) == 0 && ((1L << (_la - 129)) & -1153018544028386985L) != 0) || ((((_la - 193)) & ~0x3f) == 0 && ((1L << (_la - 193)) & -2928537194681353219L) != 0) || ((((_la - 257)) & ~0x3f) == 0 && ((1L << (_la - 257)) & 32212256745L) != 0)) {
					{
					setState(1973);
					identifier();
					setState(1978);
					_errHandler.sync(this);
					_la = _input.LA(1);
					while (_la==T__3) {
						{
						{
						setState(1974);
						match(T__3);
						setState(1975);
						identifier();
						}
						}
						setState(1980);
						_errHandler.sync(this);
						_la = _input.LA(1);
					}
					}
				}

				setState(1983);
				match(T__2);
				setState(1984);
				match(T__10);
				setState(1985);
				expression();
				}
				break;
			case 20:
				{
				_localctx = new SubqueryExpressionContext(_localctx);
				_ctx = _localctx;
				_prevctx = _localctx;
				setState(1986);
				match(T__1);
				setState(1987);
				query();
				setState(1988);
				match(T__2);
				}
				break;
			case 21:
				{
				_localctx = new ExistsContext(_localctx);
				_ctx = _localctx;
				_prevctx = _localctx;
				setState(1990);
				match(EXISTS);
				setState(1991);
				match(T__1);
				setState(1992);
				query();
				setState(1993);
				match(T__2);
				}
				break;
			case 22:
				{
				_localctx = new SimpleCaseContext(_localctx);
				_ctx = _localctx;
				_prevctx = _localctx;
				setState(1995);
				match(CASE);
				setState(1996);
				((SimpleCaseContext)_localctx).operand = expression();
				setState(1998); 
				_errHandler.sync(this);
				_la = _input.LA(1);
				do {
					{
					{
					setState(1997);
					whenClause();
					}
					}
					setState(2000); 
					_errHandler.sync(this);
					_la = _input.LA(1);
				} while ( _la==WHEN );
				setState(2004);
				_errHandler.sync(this);
				_la = _input.LA(1);
				if (_la==ELSE) {
					{
					setState(2002);
					match(ELSE);
					setState(2003);
					((SimpleCaseContext)_localctx).elseExpression = expression();
					}
				}

				setState(2006);
				match(END);
				}
				break;
			case 23:
				{
				_localctx = new SearchedCaseContext(_localctx);
				_ctx = _localctx;
				_prevctx = _localctx;
				setState(2008);
				match(CASE);
				setState(2010); 
				_errHandler.sync(this);
				_la = _input.LA(1);
				do {
					{
					{
					setState(2009);
					whenClause();
					}
					}
					setState(2012); 
					_errHandler.sync(this);
					_la = _input.LA(1);
				} while ( _la==WHEN );
				setState(2016);
				_errHandler.sync(this);
				_la = _input.LA(1);
				if (_la==ELSE) {
					{
					setState(2014);
					match(ELSE);
					setState(2015);
					((SearchedCaseContext)_localctx).elseExpression = expression();
					}
				}

				setState(2018);
				match(END);
				}
				break;
			case 24:
				{
				_localctx = new CastContext(_localctx);
				_ctx = _localctx;
				_prevctx = _localctx;
				setState(2020);
				match(CAST);
				setState(2021);
				match(T__1);
				setState(2022);
				expression();
				setState(2023);
				match(AS);
				setState(2024);
				type(0);
				setState(2025);
				match(T__2);
				}
				break;
			case 25:
				{
				_localctx = new CastContext(_localctx);
				_ctx = _localctx;
				_prevctx = _localctx;
				setState(2027);
				match(TRY_CAST);
				setState(2028);
				match(T__1);
				setState(2029);
				expression();
				setState(2030);
				match(AS);
				setState(2031);
				type(0);
				setState(2032);
				match(T__2);
				}
				break;
			case 26:
				{
				_localctx = new CastContext(_localctx);
				_ctx = _localctx;
				_prevctx = _localctx;
				setState(2034);
				match(CAST);
				setState(2035);
				match(T__1);
				setState(2036);
				expression();
				setState(2037);
				match(AS);
				setState(2040);
				_errHandler.sync(this);
				switch ( getInterpreter().adaptivePredict(_input,268,_ctx) ) {
				case 1:
					{
					setState(2038);
					match(IDENTIFIER);
					setState(2039);
					match(T__0);
					}
					break;
				}
				setState(2042);
				type(0);
				setState(2043);
				match(T__2);
				}
				break;
			case 27:
				{
				_localctx = new ArrayConstructorContext(_localctx);
				_ctx = _localctx;
				_prevctx = _localctx;
				setState(2045);
				match(ARRAY);
				setState(2046);
				match(T__11);
				setState(2055);
				_errHandler.sync(this);
				_la = _input.LA(1);
				if ((((_la) & ~0x3f) == 0 && ((1L << _la) & -304556133446578172L) != 0) || ((((_la - 64)) & ~0x3f) == 0 && ((1L << (_la - 64)) & -5424665139366696073L) != 0) || ((((_la - 129)) & ~0x3f) == 0 && ((1L << (_la - 129)) & -1153018536512192553L) != 0) || ((((_la - 193)) & ~0x3f) == 0 && ((1L << (_la - 193)) & -2928466825937175555L) != 0) || ((((_la - 257)) & ~0x3f) == 0 && ((1L << (_la - 257)) & 1133846595561L) != 0)) {
					{
					setState(2047);
					expression();
					setState(2052);
					_errHandler.sync(this);
					_la = _input.LA(1);
					while (_la==T__3) {
						{
						{
						setState(2048);
						match(T__3);
						setState(2049);
						expression();
						}
						}
						setState(2054);
						_errHandler.sync(this);
						_la = _input.LA(1);
					}
					}
				}

				setState(2057);
				match(T__12);
				}
				break;
			case 28:
				{
				_localctx = new ArrayConstructorContext(_localctx);
				_ctx = _localctx;
				_prevctx = _localctx;
				setState(2058);
				match(T__11);
				setState(2067);
				_errHandler.sync(this);
				_la = _input.LA(1);
				if ((((_la) & ~0x3f) == 0 && ((1L << _la) & -304556133446578172L) != 0) || ((((_la - 64)) & ~0x3f) == 0 && ((1L << (_la - 64)) & -5424665139366696073L) != 0) || ((((_la - 129)) & ~0x3f) == 0 && ((1L << (_la - 129)) & -1153018536512192553L) != 0) || ((((_la - 193)) & ~0x3f) == 0 && ((1L << (_la - 193)) & -2928466825937175555L) != 0) || ((((_la - 257)) & ~0x3f) == 0 && ((1L << (_la - 257)) & 1133846595561L) != 0)) {
					{
					setState(2059);
					expression();
					setState(2064);
					_errHandler.sync(this);
					_la = _input.LA(1);
					while (_la==T__3) {
						{
						{
						setState(2060);
						match(T__3);
						setState(2061);
						expression();
						}
						}
						setState(2066);
						_errHandler.sync(this);
						_la = _input.LA(1);
					}
					}
				}

				setState(2069);
				match(T__12);
				}
				break;
			case 29:
				{
				_localctx = new ColumnReferenceContext(_localctx);
				_ctx = _localctx;
				_prevctx = _localctx;
				setState(2070);
				identifier();
				}
				break;
			case 30:
				{
				_localctx = new SpecialDateTimeFunctionContext(_localctx);
				_ctx = _localctx;
				_prevctx = _localctx;
				setState(2071);
				((SpecialDateTimeFunctionContext)_localctx).name = match(CURRENT_DATE);
				}
				break;
			case 31:
				{
				_localctx = new SpecialDateTimeFunctionContext(_localctx);
				_ctx = _localctx;
				_prevctx = _localctx;
				setState(2072);
				((SpecialDateTimeFunctionContext)_localctx).name = match(CURRENT_TIME);
				setState(2076);
				_errHandler.sync(this);
				switch ( getInterpreter().adaptivePredict(_input,273,_ctx) ) {
				case 1:
					{
					setState(2073);
					match(T__1);
					setState(2074);
					((SpecialDateTimeFunctionContext)_localctx).precision = match(INTEGER_VALUE);
					setState(2075);
					match(T__2);
					}
					break;
				}
				}
				break;
			case 32:
				{
				_localctx = new SpecialDateTimeFunctionContext(_localctx);
				_ctx = _localctx;
				_prevctx = _localctx;
				setState(2078);
				((SpecialDateTimeFunctionContext)_localctx).name = match(CURRENT_TIMESTAMP);
				setState(2082);
				_errHandler.sync(this);
				switch ( getInterpreter().adaptivePredict(_input,274,_ctx) ) {
				case 1:
					{
					setState(2079);
					match(T__1);
					setState(2080);
					((SpecialDateTimeFunctionContext)_localctx).precision = match(INTEGER_VALUE);
					setState(2081);
					match(T__2);
					}
					break;
				}
				}
				break;
			case 33:
				{
				_localctx = new SpecialDateTimeFunctionContext(_localctx);
				_ctx = _localctx;
				_prevctx = _localctx;
				setState(2084);
				((SpecialDateTimeFunctionContext)_localctx).name = match(LOCALTIME);
				setState(2088);
				_errHandler.sync(this);
				switch ( getInterpreter().adaptivePredict(_input,275,_ctx) ) {
				case 1:
					{
					setState(2085);
					match(T__1);
					setState(2086);
					((SpecialDateTimeFunctionContext)_localctx).precision = match(INTEGER_VALUE);
					setState(2087);
					match(T__2);
					}
					break;
				}
				}
				break;
			case 34:
				{
				_localctx = new SpecialDateTimeFunctionContext(_localctx);
				_ctx = _localctx;
				_prevctx = _localctx;
				setState(2090);
				((SpecialDateTimeFunctionContext)_localctx).name = match(LOCALTIMESTAMP);
				setState(2094);
				_errHandler.sync(this);
				switch ( getInterpreter().adaptivePredict(_input,276,_ctx) ) {
				case 1:
					{
					setState(2091);
					match(T__1);
					setState(2092);
					((SpecialDateTimeFunctionContext)_localctx).precision = match(INTEGER_VALUE);
					setState(2093);
					match(T__2);
					}
					break;
				}
				}
				break;
			case 35:
				{
				_localctx = new CurrentUserContext(_localctx);
				_ctx = _localctx;
				_prevctx = _localctx;
				setState(2096);
				((CurrentUserContext)_localctx).name = match(CURRENT_USER);
				}
				break;
			case 36:
				{
				_localctx = new CurrentCatalogContext(_localctx);
				_ctx = _localctx;
				_prevctx = _localctx;
				setState(2097);
				((CurrentCatalogContext)_localctx).name = match(CURRENT_CATALOG);
				}
				break;
			case 37:
				{
				_localctx = new CurrentSchemaContext(_localctx);
				_ctx = _localctx;
				_prevctx = _localctx;
				setState(2101);
				_errHandler.sync(this);
				_la = _input.LA(1);
				if ((((_la) & ~0x3f) == 0 && ((1L << _la) & -9203672295665565696L) != 0) || ((((_la - 64)) & ~0x3f) == 0 && ((1L << (_la - 64)) & -5424682731988948105L) != 0) || ((((_la - 129)) & ~0x3f) == 0 && ((1L << (_la - 129)) & -1153018544028386985L) != 0) || ((((_la - 193)) & ~0x3f) == 0 && ((1L << (_la - 193)) & -2928537194681353219L) != 0) || ((((_la - 257)) & ~0x3f) == 0 && ((1L << (_la - 257)) & 32212256745L) != 0)) {
					{
					setState(2098);
					identifier();
					setState(2099);
					match(T__0);
					}
				}

				setState(2103);
				((CurrentSchemaContext)_localctx).name = match(CURRENT_SCHEMA);
				setState(2106);
				_errHandler.sync(this);
				switch ( getInterpreter().adaptivePredict(_input,278,_ctx) ) {
				case 1:
					{
					setState(2104);
					match(T__1);
					setState(2105);
					match(T__2);
					}
					break;
				}
				}
				break;
			case 38:
				{
				_localctx = new CurrentPathContext(_localctx);
				_ctx = _localctx;
				_prevctx = _localctx;
				setState(2108);
				((CurrentPathContext)_localctx).name = match(CURRENT_PATH);
				}
				break;
			case 39:
				{
				_localctx = new SubstringContext(_localctx);
				_ctx = _localctx;
				_prevctx = _localctx;
				setState(2109);
				match(SUBSTRING);
				setState(2110);
				match(T__1);
				setState(2111);
				valueExpression(0);
				setState(2112);
				match(FROM);
				setState(2113);
				valueExpression(0);
				setState(2116);
				_errHandler.sync(this);
				_la = _input.LA(1);
				if (_la==FOR) {
					{
					setState(2114);
					match(FOR);
					setState(2115);
					valueExpression(0);
					}
				}

				setState(2118);
				match(T__2);
				}
				break;
			case 40:
				{
				_localctx = new NormalizeContext(_localctx);
				_ctx = _localctx;
				_prevctx = _localctx;
				setState(2120);
				match(NORMALIZE);
				setState(2121);
				match(T__1);
				setState(2122);
				valueExpression(0);
				setState(2125);
				_errHandler.sync(this);
				_la = _input.LA(1);
				if (_la==T__3) {
					{
					setState(2123);
					match(T__3);
					setState(2124);
					normalForm();
					}
				}

				setState(2127);
				match(T__2);
				}
				break;
			case 41:
				{
				_localctx = new ExtractContext(_localctx);
				_ctx = _localctx;
				_prevctx = _localctx;
				setState(2129);
				match(EXTRACT);
				setState(2130);
				match(T__1);
				setState(2131);
				identifier();
				setState(2132);
				match(FROM);
				setState(2133);
				valueExpression(0);
				setState(2134);
				match(T__2);
				}
				break;
			case 42:
				{
				_localctx = new ParenthesizedExpressionContext(_localctx);
				_ctx = _localctx;
				_prevctx = _localctx;
				setState(2136);
				match(T__1);
				setState(2137);
				expression();
				setState(2138);
				match(T__2);
				}
				break;
			case 43:
				{
				_localctx = new GroupingOperationContext(_localctx);
				_ctx = _localctx;
				_prevctx = _localctx;
				setState(2140);
				match(GROUPING);
				setState(2141);
				match(T__1);
				setState(2150);
				_errHandler.sync(this);
				_la = _input.LA(1);
				if ((((_la) & ~0x3f) == 0 && ((1L << _la) & -9203672295665565696L) != 0) || ((((_la - 64)) & ~0x3f) == 0 && ((1L << (_la - 64)) & -5424682731988948105L) != 0) || ((((_la - 129)) & ~0x3f) == 0 && ((1L << (_la - 129)) & -1153018544028386985L) != 0) || ((((_la - 193)) & ~0x3f) == 0 && ((1L << (_la - 193)) & -2928537194681353219L) != 0) || ((((_la - 257)) & ~0x3f) == 0 && ((1L << (_la - 257)) & 32212256745L) != 0)) {
					{
					setState(2142);
					qualifiedName();
					setState(2147);
					_errHandler.sync(this);
					_la = _input.LA(1);
					while (_la==T__3) {
						{
						{
						setState(2143);
						match(T__3);
						setState(2144);
						qualifiedName();
						}
						}
						setState(2149);
						_errHandler.sync(this);
						_la = _input.LA(1);
					}
					}
				}

				setState(2152);
				match(T__2);
				}
				break;
			}
			_ctx.stop = _input.LT(-1);
			setState(2172);
			_errHandler.sync(this);
			_alt = getInterpreter().adaptivePredict(_input,286,_ctx);
			while ( _alt!=2 && _alt!=org.antlr.v4.runtime.atn.ATN.INVALID_ALT_NUMBER ) {
				if ( _alt==1 ) {
					if ( _parseListeners!=null ) triggerExitRuleEvent();
					_prevctx = _localctx;
					{
					setState(2170);
					_errHandler.sync(this);
					switch ( getInterpreter().adaptivePredict(_input,285,_ctx) ) {
					case 1:
						{
						_localctx = new CastContext(new PrimaryExpressionContext(_parentctx, _parentState));
						pushNewRecursionContext(_localctx, _startState, RULE_primaryExpression);
						setState(2155);
						if (!(precpred(_ctx, 20))) throw new FailedPredicateException(this, "precpred(_ctx, 20)");
						setState(2156);
						match(PG_CAST);
						setState(2159);
						_errHandler.sync(this);
						switch ( getInterpreter().adaptivePredict(_input,284,_ctx) ) {
						case 1:
							{
							setState(2157);
							match(IDENTIFIER);
							setState(2158);
							match(T__0);
							}
							break;
						}
						setState(2161);
						type(0);
						}
						break;
					case 2:
						{
						_localctx = new SubscriptContext(new PrimaryExpressionContext(_parentctx, _parentState));
						((SubscriptContext)_localctx).value = _prevctx;
						pushNewRecursionContext(_localctx, _startState, RULE_primaryExpression);
						setState(2162);
						if (!(precpred(_ctx, 17))) throw new FailedPredicateException(this, "precpred(_ctx, 17)");
						setState(2163);
						match(T__11);
						setState(2164);
						((SubscriptContext)_localctx).index = valueExpression(0);
						setState(2165);
						match(T__12);
						}
						break;
					case 3:
						{
						_localctx = new DereferenceContext(new PrimaryExpressionContext(_parentctx, _parentState));
						((DereferenceContext)_localctx).base = _prevctx;
						pushNewRecursionContext(_localctx, _startState, RULE_primaryExpression);
						setState(2167);
						if (!(precpred(_ctx, 15))) throw new FailedPredicateException(this, "precpred(_ctx, 15)");
						setState(2168);
						match(T__0);
						setState(2169);
						((DereferenceContext)_localctx).fieldName = identifier();
						}
						break;
					}
					} 
				}
				setState(2174);
				_errHandler.sync(this);
				_alt = getInterpreter().adaptivePredict(_input,286,_ctx);
			}
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			unrollRecursionContexts(_parentctx);
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class ProcessingModeContext extends ParserRuleContext {
		public TerminalNode RUNNING() { return getToken(SqlBaseParser.RUNNING, 0); }
		public TerminalNode FINAL() { return getToken(SqlBaseParser.FINAL, 0); }
		public ProcessingModeContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_processingMode; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterProcessingMode(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitProcessingMode(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitProcessingMode(this);
			else return visitor.visitChildren(this);
		}
	}

	public final ProcessingModeContext processingMode() throws RecognitionException {
		ProcessingModeContext _localctx = new ProcessingModeContext(_ctx, getState());
		enterRule(_localctx, 108, RULE_processingMode);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(2175);
			_la = _input.LA(1);
			if ( !(_la==FINAL || _la==RUNNING) ) {
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

	@SuppressWarnings("CheckReturnValue")
	public static class NullTreatmentContext extends ParserRuleContext {
		public TerminalNode IGNORE() { return getToken(SqlBaseParser.IGNORE, 0); }
		public TerminalNode NULLS() { return getToken(SqlBaseParser.NULLS, 0); }
		public TerminalNode RESPECT() { return getToken(SqlBaseParser.RESPECT, 0); }
		public NullTreatmentContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_nullTreatment; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterNullTreatment(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitNullTreatment(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitNullTreatment(this);
			else return visitor.visitChildren(this);
		}
	}

	public final NullTreatmentContext nullTreatment() throws RecognitionException {
		NullTreatmentContext _localctx = new NullTreatmentContext(_ctx, getState());
		enterRule(_localctx, 110, RULE_nullTreatment);
		try {
			setState(2181);
			_errHandler.sync(this);
			switch (_input.LA(1)) {
			case IGNORE:
				enterOuterAlt(_localctx, 1);
				{
				setState(2177);
				match(IGNORE);
				setState(2178);
				match(NULLS);
				}
				break;
			case RESPECT:
				enterOuterAlt(_localctx, 2);
				{
				setState(2179);
				match(RESPECT);
				setState(2180);
				match(NULLS);
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
	public static class StringContext extends ParserRuleContext {
		public StringContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_string; }
	 
		public StringContext() { }
		public void copyFrom(StringContext ctx) {
			super.copyFrom(ctx);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class EscapedCharsStringLiteralContext extends StringContext {
		public TerminalNode ESCAPED_STRING() { return getToken(SqlBaseParser.ESCAPED_STRING, 0); }
		public EscapedCharsStringLiteralContext(StringContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterEscapedCharsStringLiteral(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitEscapedCharsStringLiteral(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitEscapedCharsStringLiteral(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class UnicodeStringLiteralContext extends StringContext {
		public TerminalNode UNICODE_STRING() { return getToken(SqlBaseParser.UNICODE_STRING, 0); }
		public TerminalNode UESCAPE() { return getToken(SqlBaseParser.UESCAPE, 0); }
		public TerminalNode STRING() { return getToken(SqlBaseParser.STRING, 0); }
		public UnicodeStringLiteralContext(StringContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterUnicodeStringLiteral(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitUnicodeStringLiteral(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitUnicodeStringLiteral(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class BasicStringLiteralContext extends StringContext {
		public TerminalNode STRING() { return getToken(SqlBaseParser.STRING, 0); }
		public BasicStringLiteralContext(StringContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterBasicStringLiteral(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitBasicStringLiteral(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitBasicStringLiteral(this);
			else return visitor.visitChildren(this);
		}
	}

	public final StringContext string() throws RecognitionException {
		StringContext _localctx = new StringContext(_ctx, getState());
		enterRule(_localctx, 112, RULE_string);
		try {
			setState(2190);
			_errHandler.sync(this);
			switch (_input.LA(1)) {
			case STRING:
				_localctx = new BasicStringLiteralContext(_localctx);
				enterOuterAlt(_localctx, 1);
				{
				setState(2183);
				match(STRING);
				}
				break;
			case UNICODE_STRING:
				_localctx = new UnicodeStringLiteralContext(_localctx);
				enterOuterAlt(_localctx, 2);
				{
				setState(2184);
				match(UNICODE_STRING);
				setState(2187);
				_errHandler.sync(this);
				switch ( getInterpreter().adaptivePredict(_input,288,_ctx) ) {
				case 1:
					{
					setState(2185);
					match(UESCAPE);
					setState(2186);
					match(STRING);
					}
					break;
				}
				}
				break;
			case ESCAPED_STRING:
				_localctx = new EscapedCharsStringLiteralContext(_localctx);
				enterOuterAlt(_localctx, 3);
				{
				setState(2189);
				match(ESCAPED_STRING);
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
	public static class TimeZoneSpecifierContext extends ParserRuleContext {
		public TimeZoneSpecifierContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_timeZoneSpecifier; }
	 
		public TimeZoneSpecifierContext() { }
		public void copyFrom(TimeZoneSpecifierContext ctx) {
			super.copyFrom(ctx);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class TimeZoneIntervalContext extends TimeZoneSpecifierContext {
		public TerminalNode TIME() { return getToken(SqlBaseParser.TIME, 0); }
		public TerminalNode ZONE() { return getToken(SqlBaseParser.ZONE, 0); }
		public IntervalContext interval() {
			return getRuleContext(IntervalContext.class,0);
		}
		public TimeZoneIntervalContext(TimeZoneSpecifierContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterTimeZoneInterval(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitTimeZoneInterval(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitTimeZoneInterval(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class TimeZoneStringContext extends TimeZoneSpecifierContext {
		public TerminalNode TIME() { return getToken(SqlBaseParser.TIME, 0); }
		public TerminalNode ZONE() { return getToken(SqlBaseParser.ZONE, 0); }
		public StringContext string() {
			return getRuleContext(StringContext.class,0);
		}
		public TimeZoneStringContext(TimeZoneSpecifierContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterTimeZoneString(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitTimeZoneString(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitTimeZoneString(this);
			else return visitor.visitChildren(this);
		}
	}

	public final TimeZoneSpecifierContext timeZoneSpecifier() throws RecognitionException {
		TimeZoneSpecifierContext _localctx = new TimeZoneSpecifierContext(_ctx, getState());
		enterRule(_localctx, 114, RULE_timeZoneSpecifier);
		try {
			setState(2198);
			_errHandler.sync(this);
			switch ( getInterpreter().adaptivePredict(_input,290,_ctx) ) {
			case 1:
				_localctx = new TimeZoneIntervalContext(_localctx);
				enterOuterAlt(_localctx, 1);
				{
				setState(2192);
				match(TIME);
				setState(2193);
				match(ZONE);
				setState(2194);
				interval();
				}
				break;
			case 2:
				_localctx = new TimeZoneStringContext(_localctx);
				enterOuterAlt(_localctx, 2);
				{
				setState(2195);
				match(TIME);
				setState(2196);
				match(ZONE);
				setState(2197);
				string();
				}
				break;
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
	public static class ComparisonOperatorContext extends ParserRuleContext {
		public TerminalNode EQ() { return getToken(SqlBaseParser.EQ, 0); }
		public TerminalNode NEQ() { return getToken(SqlBaseParser.NEQ, 0); }
		public TerminalNode LT() { return getToken(SqlBaseParser.LT, 0); }
		public TerminalNode LTE() { return getToken(SqlBaseParser.LTE, 0); }
		public TerminalNode GT() { return getToken(SqlBaseParser.GT, 0); }
		public TerminalNode GTE() { return getToken(SqlBaseParser.GTE, 0); }
		public ComparisonOperatorContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_comparisonOperator; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterComparisonOperator(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitComparisonOperator(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitComparisonOperator(this);
			else return visitor.visitChildren(this);
		}
	}

	public final ComparisonOperatorContext comparisonOperator() throws RecognitionException {
		ComparisonOperatorContext _localctx = new ComparisonOperatorContext(_ctx, getState());
		enterRule(_localctx, 116, RULE_comparisonOperator);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(2200);
			_la = _input.LA(1);
			if ( !(((((_la - 268)) & ~0x3f) == 0 && ((1L << (_la - 268)) & 63L) != 0)) ) {
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

	@SuppressWarnings("CheckReturnValue")
	public static class ComparisonQuantifierContext extends ParserRuleContext {
		public TerminalNode ALL() { return getToken(SqlBaseParser.ALL, 0); }
		public TerminalNode SOME() { return getToken(SqlBaseParser.SOME, 0); }
		public TerminalNode ANY() { return getToken(SqlBaseParser.ANY, 0); }
		public ComparisonQuantifierContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_comparisonQuantifier; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterComparisonQuantifier(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitComparisonQuantifier(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitComparisonQuantifier(this);
			else return visitor.visitChildren(this);
		}
	}

	public final ComparisonQuantifierContext comparisonQuantifier() throws RecognitionException {
		ComparisonQuantifierContext _localctx = new ComparisonQuantifierContext(_ctx, getState());
		enterRule(_localctx, 118, RULE_comparisonQuantifier);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(2202);
			_la = _input.LA(1);
			if ( !(_la==ALL || _la==ANY || _la==SOME) ) {
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

	@SuppressWarnings("CheckReturnValue")
	public static class BooleanValueContext extends ParserRuleContext {
		public TerminalNode TRUE() { return getToken(SqlBaseParser.TRUE, 0); }
		public TerminalNode FALSE() { return getToken(SqlBaseParser.FALSE, 0); }
		public BooleanValueContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_booleanValue; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterBooleanValue(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitBooleanValue(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitBooleanValue(this);
			else return visitor.visitChildren(this);
		}
	}

	public final BooleanValueContext booleanValue() throws RecognitionException {
		BooleanValueContext _localctx = new BooleanValueContext(_ctx, getState());
		enterRule(_localctx, 120, RULE_booleanValue);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(2204);
			_la = _input.LA(1);
			if ( !(_la==FALSE || _la==TRUE) ) {
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

	@SuppressWarnings("CheckReturnValue")
	public static class IntervalContext extends ParserRuleContext {
		public Token sign;
		public IntervalFieldContext from;
		public IntervalFieldContext to;
		public TerminalNode INTERVAL() { return getToken(SqlBaseParser.INTERVAL, 0); }
		public StringContext string() {
			return getRuleContext(StringContext.class,0);
		}
		public List<IntervalFieldContext> intervalField() {
			return getRuleContexts(IntervalFieldContext.class);
		}
		public IntervalFieldContext intervalField(int i) {
			return getRuleContext(IntervalFieldContext.class,i);
		}
		public TerminalNode TO() { return getToken(SqlBaseParser.TO, 0); }
		public TerminalNode PLUS() { return getToken(SqlBaseParser.PLUS, 0); }
		public TerminalNode MINUS() { return getToken(SqlBaseParser.MINUS, 0); }
		public IntervalContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_interval; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterInterval(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitInterval(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitInterval(this);
			else return visitor.visitChildren(this);
		}
	}

	public final IntervalContext interval() throws RecognitionException {
		IntervalContext _localctx = new IntervalContext(_ctx, getState());
		enterRule(_localctx, 122, RULE_interval);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(2206);
			match(INTERVAL);
			setState(2208);
			_errHandler.sync(this);
			_la = _input.LA(1);
			if (_la==PLUS || _la==MINUS) {
				{
				setState(2207);
				((IntervalContext)_localctx).sign = _input.LT(1);
				_la = _input.LA(1);
				if ( !(_la==PLUS || _la==MINUS) ) {
					((IntervalContext)_localctx).sign = (Token)_errHandler.recoverInline(this);
				}
				else {
					if ( _input.LA(1)==Token.EOF ) matchedEOF = true;
					_errHandler.reportMatch(this);
					consume();
				}
				}
			}

			setState(2210);
			string();
			setState(2211);
			((IntervalContext)_localctx).from = intervalField();
			setState(2214);
			_errHandler.sync(this);
			switch ( getInterpreter().adaptivePredict(_input,292,_ctx) ) {
			case 1:
				{
				setState(2212);
				match(TO);
				setState(2213);
				((IntervalContext)_localctx).to = intervalField();
				}
				break;
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
	public static class IntervalFieldContext extends ParserRuleContext {
		public TerminalNode YEAR() { return getToken(SqlBaseParser.YEAR, 0); }
		public TerminalNode MONTH() { return getToken(SqlBaseParser.MONTH, 0); }
		public TerminalNode DAY() { return getToken(SqlBaseParser.DAY, 0); }
		public TerminalNode HOUR() { return getToken(SqlBaseParser.HOUR, 0); }
		public TerminalNode MINUTE() { return getToken(SqlBaseParser.MINUTE, 0); }
		public TerminalNode SECOND() { return getToken(SqlBaseParser.SECOND, 0); }
		public IntervalFieldContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_intervalField; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterIntervalField(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitIntervalField(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitIntervalField(this);
			else return visitor.visitChildren(this);
		}
	}

	public final IntervalFieldContext intervalField() throws RecognitionException {
		IntervalFieldContext _localctx = new IntervalFieldContext(_ctx, getState());
		enterRule(_localctx, 124, RULE_intervalField);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(2216);
			_la = _input.LA(1);
			if ( !(_la==DAY || _la==HOUR || _la==MINUTE || _la==MONTH || _la==SECOND || _la==YEAR) ) {
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

	@SuppressWarnings("CheckReturnValue")
	public static class NormalFormContext extends ParserRuleContext {
		public TerminalNode NFD() { return getToken(SqlBaseParser.NFD, 0); }
		public TerminalNode NFC() { return getToken(SqlBaseParser.NFC, 0); }
		public TerminalNode NFKD() { return getToken(SqlBaseParser.NFKD, 0); }
		public TerminalNode NFKC() { return getToken(SqlBaseParser.NFKC, 0); }
		public NormalFormContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_normalForm; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterNormalForm(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitNormalForm(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitNormalForm(this);
			else return visitor.visitChildren(this);
		}
	}

	public final NormalFormContext normalForm() throws RecognitionException {
		NormalFormContext _localctx = new NormalFormContext(_ctx, getState());
		enterRule(_localctx, 126, RULE_normalForm);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(2218);
			_la = _input.LA(1);
			if ( !(((((_la - 153)) & ~0x3f) == 0 && ((1L << (_la - 153)) & 15L) != 0)) ) {
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

	@SuppressWarnings("CheckReturnValue")
	public static class TypeContext extends ParserRuleContext {
		public TypeContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_type; }
	 
		public TypeContext() { }
		public void copyFrom(TypeContext ctx) {
			super.copyFrom(ctx);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class RowTypeContext extends TypeContext {
		public TerminalNode ROW() { return getToken(SqlBaseParser.ROW, 0); }
		public List<RowFieldContext> rowField() {
			return getRuleContexts(RowFieldContext.class);
		}
		public RowFieldContext rowField(int i) {
			return getRuleContext(RowFieldContext.class,i);
		}
		public RowTypeContext(TypeContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterRowType(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitRowType(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitRowType(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class IntervalTypeContext extends TypeContext {
		public IntervalFieldContext from;
		public IntervalFieldContext to;
		public TerminalNode INTERVAL() { return getToken(SqlBaseParser.INTERVAL, 0); }
		public List<IntervalFieldContext> intervalField() {
			return getRuleContexts(IntervalFieldContext.class);
		}
		public IntervalFieldContext intervalField(int i) {
			return getRuleContext(IntervalFieldContext.class,i);
		}
		public TerminalNode TO() { return getToken(SqlBaseParser.TO, 0); }
		public IntervalTypeContext(TypeContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterIntervalType(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitIntervalType(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitIntervalType(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class ArrayTypeContext extends TypeContext {
		public TypeContext type() {
			return getRuleContext(TypeContext.class,0);
		}
		public TerminalNode ARRAY() { return getToken(SqlBaseParser.ARRAY, 0); }
		public TerminalNode INTEGER_VALUE() { return getToken(SqlBaseParser.INTEGER_VALUE, 0); }
		public ArrayTypeContext(TypeContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterArrayType(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitArrayType(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitArrayType(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class DoublePrecisionTypeContext extends TypeContext {
		public TerminalNode DOUBLE() { return getToken(SqlBaseParser.DOUBLE, 0); }
		public TerminalNode PRECISION() { return getToken(SqlBaseParser.PRECISION, 0); }
		public DoublePrecisionTypeContext(TypeContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterDoublePrecisionType(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitDoublePrecisionType(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitDoublePrecisionType(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class LegacyArrayTypeContext extends TypeContext {
		public TerminalNode ARRAY() { return getToken(SqlBaseParser.ARRAY, 0); }
		public TerminalNode LT() { return getToken(SqlBaseParser.LT, 0); }
		public TypeContext type() {
			return getRuleContext(TypeContext.class,0);
		}
		public TerminalNode GT() { return getToken(SqlBaseParser.GT, 0); }
		public LegacyArrayTypeContext(TypeContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterLegacyArrayType(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitLegacyArrayType(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitLegacyArrayType(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class GenericTypeContext extends TypeContext {
		public IdentifierContext identifier() {
			return getRuleContext(IdentifierContext.class,0);
		}
		public List<TypeParameterContext> typeParameter() {
			return getRuleContexts(TypeParameterContext.class);
		}
		public TypeParameterContext typeParameter(int i) {
			return getRuleContext(TypeParameterContext.class,i);
		}
		public GenericTypeContext(TypeContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterGenericType(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitGenericType(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitGenericType(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class DateTimeTypeContext extends TypeContext {
		public Token base;
		public TypeParameterContext precision;
		public TerminalNode TIMESTAMP() { return getToken(SqlBaseParser.TIMESTAMP, 0); }
		public TerminalNode WITHOUT() { return getToken(SqlBaseParser.WITHOUT, 0); }
		public List<TerminalNode> TIME() { return getTokens(SqlBaseParser.TIME); }
		public TerminalNode TIME(int i) {
			return getToken(SqlBaseParser.TIME, i);
		}
		public TerminalNode ZONE() { return getToken(SqlBaseParser.ZONE, 0); }
		public TypeParameterContext typeParameter() {
			return getRuleContext(TypeParameterContext.class,0);
		}
		public TerminalNode WITH() { return getToken(SqlBaseParser.WITH, 0); }
		public DateTimeTypeContext(TypeContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterDateTimeType(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitDateTimeType(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitDateTimeType(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class LegacyMapTypeContext extends TypeContext {
		public TypeContext keyType;
		public TypeContext valueType;
		public TerminalNode MAP() { return getToken(SqlBaseParser.MAP, 0); }
		public TerminalNode LT() { return getToken(SqlBaseParser.LT, 0); }
		public TerminalNode GT() { return getToken(SqlBaseParser.GT, 0); }
		public List<TypeContext> type() {
			return getRuleContexts(TypeContext.class);
		}
		public TypeContext type(int i) {
			return getRuleContext(TypeContext.class,i);
		}
		public LegacyMapTypeContext(TypeContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterLegacyMapType(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitLegacyMapType(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitLegacyMapType(this);
			else return visitor.visitChildren(this);
		}
	}

	public final TypeContext type() throws RecognitionException {
		return type(0);
	}

	private TypeContext type(int _p) throws RecognitionException {
		ParserRuleContext _parentctx = _ctx;
		int _parentState = getState();
		TypeContext _localctx = new TypeContext(_ctx, _parentState);
		TypeContext _prevctx = _localctx;
		int _startState = 128;
		enterRecursionRule(_localctx, 128, RULE_type, _p);
		int _la;
		try {
			int _alt;
			enterOuterAlt(_localctx, 1);
			{
			setState(2311);
			_errHandler.sync(this);
			switch ( getInterpreter().adaptivePredict(_input,303,_ctx) ) {
			case 1:
				{
				_localctx = new RowTypeContext(_localctx);
				_ctx = _localctx;
				_prevctx = _localctx;

				setState(2221);
				match(ROW);
				setState(2222);
				match(T__1);
				setState(2223);
				rowField();
				setState(2228);
				_errHandler.sync(this);
				_la = _input.LA(1);
				while (_la==T__3) {
					{
					{
					setState(2224);
					match(T__3);
					setState(2225);
					rowField();
					}
					}
					setState(2230);
					_errHandler.sync(this);
					_la = _input.LA(1);
				}
				setState(2231);
				match(T__2);
				}
				break;
			case 2:
				{
				_localctx = new IntervalTypeContext(_localctx);
				_ctx = _localctx;
				_prevctx = _localctx;
				setState(2233);
				match(INTERVAL);
				setState(2234);
				((IntervalTypeContext)_localctx).from = intervalField();
				setState(2237);
				_errHandler.sync(this);
				switch ( getInterpreter().adaptivePredict(_input,294,_ctx) ) {
				case 1:
					{
					setState(2235);
					match(TO);
					setState(2236);
					((IntervalTypeContext)_localctx).to = intervalField();
					}
					break;
				}
				}
				break;
			case 3:
				{
				_localctx = new DateTimeTypeContext(_localctx);
				_ctx = _localctx;
				_prevctx = _localctx;
				setState(2239);
				((DateTimeTypeContext)_localctx).base = match(TIMESTAMP);
				setState(2244);
				_errHandler.sync(this);
				switch ( getInterpreter().adaptivePredict(_input,295,_ctx) ) {
				case 1:
					{
					setState(2240);
					match(T__1);
					setState(2241);
					((DateTimeTypeContext)_localctx).precision = typeParameter();
					setState(2242);
					match(T__2);
					}
					break;
				}
				setState(2249);
				_errHandler.sync(this);
				switch ( getInterpreter().adaptivePredict(_input,296,_ctx) ) {
				case 1:
					{
					setState(2246);
					match(WITHOUT);
					setState(2247);
					match(TIME);
					setState(2248);
					match(ZONE);
					}
					break;
				}
				}
				break;
			case 4:
				{
				_localctx = new DateTimeTypeContext(_localctx);
				_ctx = _localctx;
				_prevctx = _localctx;
				setState(2251);
				((DateTimeTypeContext)_localctx).base = match(TIMESTAMP);
				setState(2256);
				_errHandler.sync(this);
				_la = _input.LA(1);
				if (_la==T__1) {
					{
					setState(2252);
					match(T__1);
					setState(2253);
					((DateTimeTypeContext)_localctx).precision = typeParameter();
					setState(2254);
					match(T__2);
					}
				}

				setState(2258);
				match(WITH);
				setState(2259);
				match(TIME);
				setState(2260);
				match(ZONE);
				}
				break;
			case 5:
				{
				_localctx = new DateTimeTypeContext(_localctx);
				_ctx = _localctx;
				_prevctx = _localctx;
				setState(2261);
				((DateTimeTypeContext)_localctx).base = match(TIME);
				setState(2266);
				_errHandler.sync(this);
				switch ( getInterpreter().adaptivePredict(_input,298,_ctx) ) {
				case 1:
					{
					setState(2262);
					match(T__1);
					setState(2263);
					((DateTimeTypeContext)_localctx).precision = typeParameter();
					setState(2264);
					match(T__2);
					}
					break;
				}
				setState(2271);
				_errHandler.sync(this);
				switch ( getInterpreter().adaptivePredict(_input,299,_ctx) ) {
				case 1:
					{
					setState(2268);
					match(WITHOUT);
					setState(2269);
					match(TIME);
					setState(2270);
					match(ZONE);
					}
					break;
				}
				}
				break;
			case 6:
				{
				_localctx = new DateTimeTypeContext(_localctx);
				_ctx = _localctx;
				_prevctx = _localctx;
				setState(2273);
				((DateTimeTypeContext)_localctx).base = match(TIME);
				setState(2278);
				_errHandler.sync(this);
				_la = _input.LA(1);
				if (_la==T__1) {
					{
					setState(2274);
					match(T__1);
					setState(2275);
					((DateTimeTypeContext)_localctx).precision = typeParameter();
					setState(2276);
					match(T__2);
					}
				}

				setState(2280);
				match(WITH);
				setState(2281);
				match(TIME);
				setState(2282);
				match(ZONE);
				}
				break;
			case 7:
				{
				_localctx = new DoublePrecisionTypeContext(_localctx);
				_ctx = _localctx;
				_prevctx = _localctx;
				setState(2283);
				match(DOUBLE);
				setState(2284);
				match(PRECISION);
				}
				break;
			case 8:
				{
				_localctx = new LegacyArrayTypeContext(_localctx);
				_ctx = _localctx;
				_prevctx = _localctx;
				setState(2285);
				match(ARRAY);
				setState(2286);
				match(LT);
				setState(2287);
				type(0);
				setState(2288);
				match(GT);
				}
				break;
			case 9:
				{
				_localctx = new LegacyMapTypeContext(_localctx);
				_ctx = _localctx;
				_prevctx = _localctx;
				setState(2290);
				match(MAP);
				setState(2291);
				match(LT);
				setState(2292);
				((LegacyMapTypeContext)_localctx).keyType = type(0);
				setState(2293);
				match(T__3);
				setState(2294);
				((LegacyMapTypeContext)_localctx).valueType = type(0);
				setState(2295);
				match(GT);
				}
				break;
			case 10:
				{
				_localctx = new GenericTypeContext(_localctx);
				_ctx = _localctx;
				_prevctx = _localctx;
				setState(2297);
				identifier();
				setState(2309);
				_errHandler.sync(this);
				switch ( getInterpreter().adaptivePredict(_input,302,_ctx) ) {
				case 1:
					{
					setState(2298);
					match(T__1);
					setState(2299);
					typeParameter();
					setState(2304);
					_errHandler.sync(this);
					_la = _input.LA(1);
					while (_la==T__3) {
						{
						{
						setState(2300);
						match(T__3);
						setState(2301);
						typeParameter();
						}
						}
						setState(2306);
						_errHandler.sync(this);
						_la = _input.LA(1);
					}
					setState(2307);
					match(T__2);
					}
					break;
				}
				}
				break;
			}
			_ctx.stop = _input.LT(-1);
			setState(2322);
			_errHandler.sync(this);
			_alt = getInterpreter().adaptivePredict(_input,305,_ctx);
			while ( _alt!=2 && _alt!=org.antlr.v4.runtime.atn.ATN.INVALID_ALT_NUMBER ) {
				if ( _alt==1 ) {
					if ( _parseListeners!=null ) triggerExitRuleEvent();
					_prevctx = _localctx;
					{
					{
					_localctx = new ArrayTypeContext(new TypeContext(_parentctx, _parentState));
					pushNewRecursionContext(_localctx, _startState, RULE_type);
					setState(2313);
					if (!(precpred(_ctx, 2))) throw new FailedPredicateException(this, "precpred(_ctx, 2)");
					setState(2314);
					match(ARRAY);
					setState(2318);
					_errHandler.sync(this);
					switch ( getInterpreter().adaptivePredict(_input,304,_ctx) ) {
					case 1:
						{
						setState(2315);
						match(T__11);
						setState(2316);
						match(INTEGER_VALUE);
						setState(2317);
						match(T__12);
						}
						break;
					}
					}
					} 
				}
				setState(2324);
				_errHandler.sync(this);
				_alt = getInterpreter().adaptivePredict(_input,305,_ctx);
			}
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			unrollRecursionContexts(_parentctx);
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class RowFieldContext extends ParserRuleContext {
		public TypeContext type() {
			return getRuleContext(TypeContext.class,0);
		}
		public IdentifierContext identifier() {
			return getRuleContext(IdentifierContext.class,0);
		}
		public RowFieldContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_rowField; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterRowField(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitRowField(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitRowField(this);
			else return visitor.visitChildren(this);
		}
	}

	public final RowFieldContext rowField() throws RecognitionException {
		RowFieldContext _localctx = new RowFieldContext(_ctx, getState());
		enterRule(_localctx, 130, RULE_rowField);
		try {
			setState(2329);
			_errHandler.sync(this);
			switch ( getInterpreter().adaptivePredict(_input,306,_ctx) ) {
			case 1:
				enterOuterAlt(_localctx, 1);
				{
				setState(2325);
				type(0);
				}
				break;
			case 2:
				enterOuterAlt(_localctx, 2);
				{
				setState(2326);
				identifier();
				setState(2327);
				type(0);
				}
				break;
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
	public static class TypeParameterContext extends ParserRuleContext {
		public TerminalNode INTEGER_VALUE() { return getToken(SqlBaseParser.INTEGER_VALUE, 0); }
		public TypeContext type() {
			return getRuleContext(TypeContext.class,0);
		}
		public TypeParameterContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_typeParameter; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterTypeParameter(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitTypeParameter(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitTypeParameter(this);
			else return visitor.visitChildren(this);
		}
	}

	public final TypeParameterContext typeParameter() throws RecognitionException {
		TypeParameterContext _localctx = new TypeParameterContext(_ctx, getState());
		enterRule(_localctx, 132, RULE_typeParameter);
		try {
			setState(2333);
			_errHandler.sync(this);
			switch (_input.LA(1)) {
			case INTEGER_VALUE:
				enterOuterAlt(_localctx, 1);
				{
				setState(2331);
				match(INTEGER_VALUE);
				}
				break;
			case ADD:
			case ADMIN:
			case AFTER:
			case ALL:
			case ANALYZE:
			case ANY:
			case ARRAY:
			case ASC:
			case AT:
			case AUTHORIZATION:
			case BERNOULLI:
			case CALL:
			case CASCADE:
			case CATALOGS:
			case COLLATE:
			case COLUMN:
			case COLUMNS:
			case COMMENT:
			case COMMIT:
			case COMMITTED:
			case COUNT:
			case CURRENT:
			case CURSOR:
			case DATA:
			case DATE:
			case DAY:
			case DECLARE:
			case DEFAULT:
			case DEFINER:
			case DENY:
			case DESC:
			case DEFINE:
			case DISTRIBUTED:
			case DOUBLE:
			case EMPTY:
			case EPOCH:
			case ERROR:
			case EXCLUDING:
			case EXPLAIN:
			case FETCH:
			case FILTER:
			case FINAL:
			case FIRST:
			case FOLLOWING:
			case FORMAT:
			case FUNCTIONS:
			case GRANT:
			case GRANTED:
			case GRANTS:
			case GRAPHVIZ:
			case GROUPS:
			case HOUR:
			case IF:
			case IGNORE:
			case IMPERSONATE:
			case INCLUDING:
			case INITIAL:
			case INPUT:
			case INTERVAL:
			case INVOKER:
			case IO:
			case ISOLATION:
			case JSON:
			case LAST:
			case LATERAL:
			case LEVEL:
			case LIMIT:
			case LOCAL:
			case LOGICAL:
			case MAP:
			case MATCH:
			case MATCHED:
			case MATCHES:
			case MATCH_RECOGNIZE:
			case MATERIALIZED:
			case MEASURES:
			case MERGE:
			case MINUTE:
			case MONTH:
			case NEXT:
			case NFC:
			case NFD:
			case NFKC:
			case NFKD:
			case NO:
			case NONE:
			case NULLIF:
			case NULLS:
			case OFFSET:
			case OMIT:
			case OF:
			case ONE:
			case ONLY:
			case OPERATOR:
			case OPTION:
			case ORDINALITY:
			case OUTPUT:
			case OVER:
			case OVERFLOW:
			case PARTITION:
			case PARTITIONS:
			case PAST:
			case PATH:
			case PATTERN:
			case PER:
			case PERMUTE:
			case POSITION:
			case PRECEDING:
			case PRECISION:
			case PRIVILEGES:
			case PROPERTIES:
			case RANGE:
			case READ:
			case REFRESH:
			case RENAME:
			case REPEATABLE:
			case REPLACE:
			case RESET:
			case RESPECT:
			case RESTRICT:
			case REVOKE:
			case ROLE:
			case ROLES:
			case ROLLBACK:
			case ROW:
			case ROWS:
			case RUNNING:
			case SCHEMA:
			case SCHEMAS:
			case SECOND:
			case SECURITY:
			case SEEK:
			case SERIALIZABLE:
			case SESSION:
			case SESSION_USER:
			case SET:
			case SETS:
			case SHOW:
			case SOME:
			case START:
			case STATS:
			case SUBSET:
			case SUBSTRING:
			case SYSTEM:
			case TABLES:
			case TABLESAMPLE:
			case TEXT:
			case TIES:
			case TIME:
			case TIMESTAMP:
			case TO:
			case TRANSACTION:
			case TRUNCATE:
			case TRY_CAST:
			case TYPE:
			case UNBOUNDED:
			case UNCOMMITTED:
			case UNMATCHED:
			case UPDATE:
			case USE:
			case USER:
			case VALIDATE:
			case VERBOSE:
			case VERSION:
			case VIEW:
			case WINDOW:
			case WITHIN:
			case WITHOUT:
			case WORK:
			case WRITE:
			case YEAR:
			case ZONE:
			case IDENTIFIER:
			case DIGIT_IDENTIFIER:
			case QUOTED_IDENTIFIER:
			case BACKQUOTED_IDENTIFIER:
				enterOuterAlt(_localctx, 2);
				{
				setState(2332);
				type(0);
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
	public static class WhenClauseContext extends ParserRuleContext {
		public ExpressionContext condition;
		public ExpressionContext result;
		public TerminalNode WHEN() { return getToken(SqlBaseParser.WHEN, 0); }
		public TerminalNode THEN() { return getToken(SqlBaseParser.THEN, 0); }
		public List<ExpressionContext> expression() {
			return getRuleContexts(ExpressionContext.class);
		}
		public ExpressionContext expression(int i) {
			return getRuleContext(ExpressionContext.class,i);
		}
		public WhenClauseContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_whenClause; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterWhenClause(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitWhenClause(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitWhenClause(this);
			else return visitor.visitChildren(this);
		}
	}

	public final WhenClauseContext whenClause() throws RecognitionException {
		WhenClauseContext _localctx = new WhenClauseContext(_ctx, getState());
		enterRule(_localctx, 134, RULE_whenClause);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(2335);
			match(WHEN);
			setState(2336);
			((WhenClauseContext)_localctx).condition = expression();
			setState(2337);
			match(THEN);
			setState(2338);
			((WhenClauseContext)_localctx).result = expression();
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
	public static class FilterContext extends ParserRuleContext {
		public TerminalNode FILTER() { return getToken(SqlBaseParser.FILTER, 0); }
		public TerminalNode WHERE() { return getToken(SqlBaseParser.WHERE, 0); }
		public BooleanExpressionContext booleanExpression() {
			return getRuleContext(BooleanExpressionContext.class,0);
		}
		public FilterContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_filter; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterFilter(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitFilter(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitFilter(this);
			else return visitor.visitChildren(this);
		}
	}

	public final FilterContext filter() throws RecognitionException {
		FilterContext _localctx = new FilterContext(_ctx, getState());
		enterRule(_localctx, 136, RULE_filter);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(2340);
			match(FILTER);
			setState(2341);
			match(T__1);
			setState(2342);
			match(WHERE);
			setState(2343);
			booleanExpression(0);
			setState(2344);
			match(T__2);
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
	public static class MergeCaseContext extends ParserRuleContext {
		public MergeCaseContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_mergeCase; }
	 
		public MergeCaseContext() { }
		public void copyFrom(MergeCaseContext ctx) {
			super.copyFrom(ctx);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class MergeInsertContext extends MergeCaseContext {
		public ExpressionContext condition;
		public IdentifierContext identifier;
		public List<IdentifierContext> targets = new ArrayList<IdentifierContext>();
		public ExpressionContext expression;
		public List<ExpressionContext> values = new ArrayList<ExpressionContext>();
		public TerminalNode WHEN() { return getToken(SqlBaseParser.WHEN, 0); }
		public TerminalNode NOT() { return getToken(SqlBaseParser.NOT, 0); }
		public TerminalNode MATCHED() { return getToken(SqlBaseParser.MATCHED, 0); }
		public TerminalNode THEN() { return getToken(SqlBaseParser.THEN, 0); }
		public TerminalNode INSERT() { return getToken(SqlBaseParser.INSERT, 0); }
		public TerminalNode VALUES() { return getToken(SqlBaseParser.VALUES, 0); }
		public List<ExpressionContext> expression() {
			return getRuleContexts(ExpressionContext.class);
		}
		public ExpressionContext expression(int i) {
			return getRuleContext(ExpressionContext.class,i);
		}
		public TerminalNode AND() { return getToken(SqlBaseParser.AND, 0); }
		public List<IdentifierContext> identifier() {
			return getRuleContexts(IdentifierContext.class);
		}
		public IdentifierContext identifier(int i) {
			return getRuleContext(IdentifierContext.class,i);
		}
		public MergeInsertContext(MergeCaseContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterMergeInsert(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitMergeInsert(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitMergeInsert(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class MergeUpdateContext extends MergeCaseContext {
		public ExpressionContext condition;
		public IdentifierContext identifier;
		public List<IdentifierContext> targets = new ArrayList<IdentifierContext>();
		public ExpressionContext expression;
		public List<ExpressionContext> values = new ArrayList<ExpressionContext>();
		public TerminalNode WHEN() { return getToken(SqlBaseParser.WHEN, 0); }
		public TerminalNode MATCHED() { return getToken(SqlBaseParser.MATCHED, 0); }
		public TerminalNode THEN() { return getToken(SqlBaseParser.THEN, 0); }
		public TerminalNode UPDATE() { return getToken(SqlBaseParser.UPDATE, 0); }
		public TerminalNode SET() { return getToken(SqlBaseParser.SET, 0); }
		public List<TerminalNode> EQ() { return getTokens(SqlBaseParser.EQ); }
		public TerminalNode EQ(int i) {
			return getToken(SqlBaseParser.EQ, i);
		}
		public List<IdentifierContext> identifier() {
			return getRuleContexts(IdentifierContext.class);
		}
		public IdentifierContext identifier(int i) {
			return getRuleContext(IdentifierContext.class,i);
		}
		public List<ExpressionContext> expression() {
			return getRuleContexts(ExpressionContext.class);
		}
		public ExpressionContext expression(int i) {
			return getRuleContext(ExpressionContext.class,i);
		}
		public TerminalNode AND() { return getToken(SqlBaseParser.AND, 0); }
		public MergeUpdateContext(MergeCaseContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterMergeUpdate(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitMergeUpdate(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitMergeUpdate(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class MergeDeleteContext extends MergeCaseContext {
		public ExpressionContext condition;
		public TerminalNode WHEN() { return getToken(SqlBaseParser.WHEN, 0); }
		public TerminalNode MATCHED() { return getToken(SqlBaseParser.MATCHED, 0); }
		public TerminalNode THEN() { return getToken(SqlBaseParser.THEN, 0); }
		public TerminalNode DELETE() { return getToken(SqlBaseParser.DELETE, 0); }
		public TerminalNode AND() { return getToken(SqlBaseParser.AND, 0); }
		public ExpressionContext expression() {
			return getRuleContext(ExpressionContext.class,0);
		}
		public MergeDeleteContext(MergeCaseContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterMergeDelete(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitMergeDelete(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitMergeDelete(this);
			else return visitor.visitChildren(this);
		}
	}

	public final MergeCaseContext mergeCase() throws RecognitionException {
		MergeCaseContext _localctx = new MergeCaseContext(_ctx, getState());
		enterRule(_localctx, 138, RULE_mergeCase);
		int _la;
		try {
			setState(2410);
			_errHandler.sync(this);
			switch ( getInterpreter().adaptivePredict(_input,315,_ctx) ) {
			case 1:
				_localctx = new MergeUpdateContext(_localctx);
				enterOuterAlt(_localctx, 1);
				{
				setState(2346);
				match(WHEN);
				setState(2347);
				match(MATCHED);
				setState(2350);
				_errHandler.sync(this);
				_la = _input.LA(1);
				if (_la==AND) {
					{
					setState(2348);
					match(AND);
					setState(2349);
					((MergeUpdateContext)_localctx).condition = expression();
					}
				}

				setState(2352);
				match(THEN);
				setState(2353);
				match(UPDATE);
				setState(2354);
				match(SET);
				setState(2355);
				((MergeUpdateContext)_localctx).identifier = identifier();
				((MergeUpdateContext)_localctx).targets.add(((MergeUpdateContext)_localctx).identifier);
				setState(2356);
				match(EQ);
				setState(2357);
				((MergeUpdateContext)_localctx).expression = expression();
				((MergeUpdateContext)_localctx).values.add(((MergeUpdateContext)_localctx).expression);
				setState(2365);
				_errHandler.sync(this);
				_la = _input.LA(1);
				while (_la==T__3) {
					{
					{
					setState(2358);
					match(T__3);
					setState(2359);
					((MergeUpdateContext)_localctx).identifier = identifier();
					((MergeUpdateContext)_localctx).targets.add(((MergeUpdateContext)_localctx).identifier);
					setState(2360);
					match(EQ);
					setState(2361);
					((MergeUpdateContext)_localctx).expression = expression();
					((MergeUpdateContext)_localctx).values.add(((MergeUpdateContext)_localctx).expression);
					}
					}
					setState(2367);
					_errHandler.sync(this);
					_la = _input.LA(1);
				}
				}
				break;
			case 2:
				_localctx = new MergeDeleteContext(_localctx);
				enterOuterAlt(_localctx, 2);
				{
				setState(2368);
				match(WHEN);
				setState(2369);
				match(MATCHED);
				setState(2372);
				_errHandler.sync(this);
				_la = _input.LA(1);
				if (_la==AND) {
					{
					setState(2370);
					match(AND);
					setState(2371);
					((MergeDeleteContext)_localctx).condition = expression();
					}
				}

				setState(2374);
				match(THEN);
				setState(2375);
				match(DELETE);
				}
				break;
			case 3:
				_localctx = new MergeInsertContext(_localctx);
				enterOuterAlt(_localctx, 3);
				{
				setState(2376);
				match(WHEN);
				setState(2377);
				match(NOT);
				setState(2378);
				match(MATCHED);
				setState(2381);
				_errHandler.sync(this);
				_la = _input.LA(1);
				if (_la==AND) {
					{
					setState(2379);
					match(AND);
					setState(2380);
					((MergeInsertContext)_localctx).condition = expression();
					}
				}

				setState(2383);
				match(THEN);
				setState(2384);
				match(INSERT);
				setState(2396);
				_errHandler.sync(this);
				_la = _input.LA(1);
				if (_la==T__1) {
					{
					setState(2385);
					match(T__1);
					setState(2386);
					((MergeInsertContext)_localctx).identifier = identifier();
					((MergeInsertContext)_localctx).targets.add(((MergeInsertContext)_localctx).identifier);
					setState(2391);
					_errHandler.sync(this);
					_la = _input.LA(1);
					while (_la==T__3) {
						{
						{
						setState(2387);
						match(T__3);
						setState(2388);
						((MergeInsertContext)_localctx).identifier = identifier();
						((MergeInsertContext)_localctx).targets.add(((MergeInsertContext)_localctx).identifier);
						}
						}
						setState(2393);
						_errHandler.sync(this);
						_la = _input.LA(1);
					}
					setState(2394);
					match(T__2);
					}
				}

				setState(2398);
				match(VALUES);
				setState(2399);
				match(T__1);
				setState(2400);
				((MergeInsertContext)_localctx).expression = expression();
				((MergeInsertContext)_localctx).values.add(((MergeInsertContext)_localctx).expression);
				setState(2405);
				_errHandler.sync(this);
				_la = _input.LA(1);
				while (_la==T__3) {
					{
					{
					setState(2401);
					match(T__3);
					setState(2402);
					((MergeInsertContext)_localctx).expression = expression();
					((MergeInsertContext)_localctx).values.add(((MergeInsertContext)_localctx).expression);
					}
					}
					setState(2407);
					_errHandler.sync(this);
					_la = _input.LA(1);
				}
				setState(2408);
				match(T__2);
				}
				break;
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
	public static class OverContext extends ParserRuleContext {
		public IdentifierContext windowName;
		public TerminalNode OVER() { return getToken(SqlBaseParser.OVER, 0); }
		public WindowSpecificationContext windowSpecification() {
			return getRuleContext(WindowSpecificationContext.class,0);
		}
		public IdentifierContext identifier() {
			return getRuleContext(IdentifierContext.class,0);
		}
		public OverContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_over; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterOver(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitOver(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitOver(this);
			else return visitor.visitChildren(this);
		}
	}

	public final OverContext over() throws RecognitionException {
		OverContext _localctx = new OverContext(_ctx, getState());
		enterRule(_localctx, 140, RULE_over);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(2412);
			match(OVER);
			setState(2418);
			_errHandler.sync(this);
			switch (_input.LA(1)) {
			case ADD:
			case ADMIN:
			case AFTER:
			case ALL:
			case ANALYZE:
			case ANY:
			case ARRAY:
			case ASC:
			case AT:
			case AUTHORIZATION:
			case BERNOULLI:
			case CALL:
			case CASCADE:
			case CATALOGS:
			case COLLATE:
			case COLUMN:
			case COLUMNS:
			case COMMENT:
			case COMMIT:
			case COMMITTED:
			case COUNT:
			case CURRENT:
			case CURSOR:
			case DATA:
			case DATE:
			case DAY:
			case DECLARE:
			case DEFAULT:
			case DEFINER:
			case DENY:
			case DESC:
			case DEFINE:
			case DISTRIBUTED:
			case DOUBLE:
			case EMPTY:
			case EPOCH:
			case ERROR:
			case EXCLUDING:
			case EXPLAIN:
			case FETCH:
			case FILTER:
			case FINAL:
			case FIRST:
			case FOLLOWING:
			case FORMAT:
			case FUNCTIONS:
			case GRANT:
			case GRANTED:
			case GRANTS:
			case GRAPHVIZ:
			case GROUPS:
			case HOUR:
			case IF:
			case IGNORE:
			case IMPERSONATE:
			case INCLUDING:
			case INITIAL:
			case INPUT:
			case INTERVAL:
			case INVOKER:
			case IO:
			case ISOLATION:
			case JSON:
			case LAST:
			case LATERAL:
			case LEVEL:
			case LIMIT:
			case LOCAL:
			case LOGICAL:
			case MAP:
			case MATCH:
			case MATCHED:
			case MATCHES:
			case MATCH_RECOGNIZE:
			case MATERIALIZED:
			case MEASURES:
			case MERGE:
			case MINUTE:
			case MONTH:
			case NEXT:
			case NFC:
			case NFD:
			case NFKC:
			case NFKD:
			case NO:
			case NONE:
			case NULLIF:
			case NULLS:
			case OFFSET:
			case OMIT:
			case OF:
			case ONE:
			case ONLY:
			case OPERATOR:
			case OPTION:
			case ORDINALITY:
			case OUTPUT:
			case OVER:
			case OVERFLOW:
			case PARTITION:
			case PARTITIONS:
			case PAST:
			case PATH:
			case PATTERN:
			case PER:
			case PERMUTE:
			case POSITION:
			case PRECEDING:
			case PRECISION:
			case PRIVILEGES:
			case PROPERTIES:
			case RANGE:
			case READ:
			case REFRESH:
			case RENAME:
			case REPEATABLE:
			case REPLACE:
			case RESET:
			case RESPECT:
			case RESTRICT:
			case REVOKE:
			case ROLE:
			case ROLES:
			case ROLLBACK:
			case ROW:
			case ROWS:
			case RUNNING:
			case SCHEMA:
			case SCHEMAS:
			case SECOND:
			case SECURITY:
			case SEEK:
			case SERIALIZABLE:
			case SESSION:
			case SESSION_USER:
			case SET:
			case SETS:
			case SHOW:
			case SOME:
			case START:
			case STATS:
			case SUBSET:
			case SUBSTRING:
			case SYSTEM:
			case TABLES:
			case TABLESAMPLE:
			case TEXT:
			case TIES:
			case TIME:
			case TIMESTAMP:
			case TO:
			case TRANSACTION:
			case TRUNCATE:
			case TRY_CAST:
			case TYPE:
			case UNBOUNDED:
			case UNCOMMITTED:
			case UNMATCHED:
			case UPDATE:
			case USE:
			case USER:
			case VALIDATE:
			case VERBOSE:
			case VERSION:
			case VIEW:
			case WINDOW:
			case WITHIN:
			case WITHOUT:
			case WORK:
			case WRITE:
			case YEAR:
			case ZONE:
			case IDENTIFIER:
			case DIGIT_IDENTIFIER:
			case QUOTED_IDENTIFIER:
			case BACKQUOTED_IDENTIFIER:
				{
				setState(2413);
				((OverContext)_localctx).windowName = identifier();
				}
				break;
			case T__1:
				{
				setState(2414);
				match(T__1);
				setState(2415);
				windowSpecification();
				setState(2416);
				match(T__2);
				}
				break;
			default:
				throw new NoViableAltException(this);
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
	public static class WindowFrameContext extends ParserRuleContext {
		public FrameExtentContext frameExtent() {
			return getRuleContext(FrameExtentContext.class,0);
		}
		public TerminalNode MEASURES() { return getToken(SqlBaseParser.MEASURES, 0); }
		public List<MeasureDefinitionContext> measureDefinition() {
			return getRuleContexts(MeasureDefinitionContext.class);
		}
		public MeasureDefinitionContext measureDefinition(int i) {
			return getRuleContext(MeasureDefinitionContext.class,i);
		}
		public TerminalNode AFTER() { return getToken(SqlBaseParser.AFTER, 0); }
		public TerminalNode MATCH() { return getToken(SqlBaseParser.MATCH, 0); }
		public SkipToContext skipTo() {
			return getRuleContext(SkipToContext.class,0);
		}
		public TerminalNode PATTERN() { return getToken(SqlBaseParser.PATTERN, 0); }
		public RowPatternContext rowPattern() {
			return getRuleContext(RowPatternContext.class,0);
		}
		public TerminalNode SUBSET() { return getToken(SqlBaseParser.SUBSET, 0); }
		public List<SubsetDefinitionContext> subsetDefinition() {
			return getRuleContexts(SubsetDefinitionContext.class);
		}
		public SubsetDefinitionContext subsetDefinition(int i) {
			return getRuleContext(SubsetDefinitionContext.class,i);
		}
		public TerminalNode DEFINE() { return getToken(SqlBaseParser.DEFINE, 0); }
		public List<VariableDefinitionContext> variableDefinition() {
			return getRuleContexts(VariableDefinitionContext.class);
		}
		public VariableDefinitionContext variableDefinition(int i) {
			return getRuleContext(VariableDefinitionContext.class,i);
		}
		public TerminalNode INITIAL() { return getToken(SqlBaseParser.INITIAL, 0); }
		public TerminalNode SEEK() { return getToken(SqlBaseParser.SEEK, 0); }
		public WindowFrameContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_windowFrame; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterWindowFrame(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitWindowFrame(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitWindowFrame(this);
			else return visitor.visitChildren(this);
		}
	}

	public final WindowFrameContext windowFrame() throws RecognitionException {
		WindowFrameContext _localctx = new WindowFrameContext(_ctx, getState());
		enterRule(_localctx, 142, RULE_windowFrame);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(2429);
			_errHandler.sync(this);
			_la = _input.LA(1);
			if (_la==MEASURES) {
				{
				setState(2420);
				match(MEASURES);
				setState(2421);
				measureDefinition();
				setState(2426);
				_errHandler.sync(this);
				_la = _input.LA(1);
				while (_la==T__3) {
					{
					{
					setState(2422);
					match(T__3);
					setState(2423);
					measureDefinition();
					}
					}
					setState(2428);
					_errHandler.sync(this);
					_la = _input.LA(1);
				}
				}
			}

			setState(2431);
			frameExtent();
			setState(2435);
			_errHandler.sync(this);
			_la = _input.LA(1);
			if (_la==AFTER) {
				{
				setState(2432);
				match(AFTER);
				setState(2433);
				match(MATCH);
				setState(2434);
				skipTo();
				}
			}

			setState(2438);
			_errHandler.sync(this);
			_la = _input.LA(1);
			if (_la==INITIAL || _la==SEEK) {
				{
				setState(2437);
				_la = _input.LA(1);
				if ( !(_la==INITIAL || _la==SEEK) ) {
				_errHandler.recoverInline(this);
				}
				else {
					if ( _input.LA(1)==Token.EOF ) matchedEOF = true;
					_errHandler.reportMatch(this);
					consume();
				}
				}
			}

			setState(2445);
			_errHandler.sync(this);
			_la = _input.LA(1);
			if (_la==PATTERN) {
				{
				setState(2440);
				match(PATTERN);
				setState(2441);
				match(T__1);
				setState(2442);
				rowPattern(0);
				setState(2443);
				match(T__2);
				}
			}

			setState(2456);
			_errHandler.sync(this);
			_la = _input.LA(1);
			if (_la==SUBSET) {
				{
				setState(2447);
				match(SUBSET);
				setState(2448);
				subsetDefinition();
				setState(2453);
				_errHandler.sync(this);
				_la = _input.LA(1);
				while (_la==T__3) {
					{
					{
					setState(2449);
					match(T__3);
					setState(2450);
					subsetDefinition();
					}
					}
					setState(2455);
					_errHandler.sync(this);
					_la = _input.LA(1);
				}
				}
			}

			setState(2467);
			_errHandler.sync(this);
			_la = _input.LA(1);
			if (_la==DEFINE) {
				{
				setState(2458);
				match(DEFINE);
				setState(2459);
				variableDefinition();
				setState(2464);
				_errHandler.sync(this);
				_la = _input.LA(1);
				while (_la==T__3) {
					{
					{
					setState(2460);
					match(T__3);
					setState(2461);
					variableDefinition();
					}
					}
					setState(2466);
					_errHandler.sync(this);
					_la = _input.LA(1);
				}
				}
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
	public static class FrameExtentContext extends ParserRuleContext {
		public Token frameType;
		public FrameBoundContext start;
		public FrameBoundContext end;
		public TerminalNode RANGE() { return getToken(SqlBaseParser.RANGE, 0); }
		public List<FrameBoundContext> frameBound() {
			return getRuleContexts(FrameBoundContext.class);
		}
		public FrameBoundContext frameBound(int i) {
			return getRuleContext(FrameBoundContext.class,i);
		}
		public TerminalNode ROWS() { return getToken(SqlBaseParser.ROWS, 0); }
		public TerminalNode GROUPS() { return getToken(SqlBaseParser.GROUPS, 0); }
		public TerminalNode BETWEEN() { return getToken(SqlBaseParser.BETWEEN, 0); }
		public TerminalNode AND() { return getToken(SqlBaseParser.AND, 0); }
		public FrameExtentContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_frameExtent; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterFrameExtent(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitFrameExtent(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitFrameExtent(this);
			else return visitor.visitChildren(this);
		}
	}

	public final FrameExtentContext frameExtent() throws RecognitionException {
		FrameExtentContext _localctx = new FrameExtentContext(_ctx, getState());
		enterRule(_localctx, 144, RULE_frameExtent);
		try {
			setState(2493);
			_errHandler.sync(this);
			switch ( getInterpreter().adaptivePredict(_input,326,_ctx) ) {
			case 1:
				enterOuterAlt(_localctx, 1);
				{
				setState(2469);
				((FrameExtentContext)_localctx).frameType = match(RANGE);
				setState(2470);
				((FrameExtentContext)_localctx).start = frameBound();
				}
				break;
			case 2:
				enterOuterAlt(_localctx, 2);
				{
				setState(2471);
				((FrameExtentContext)_localctx).frameType = match(ROWS);
				setState(2472);
				((FrameExtentContext)_localctx).start = frameBound();
				}
				break;
			case 3:
				enterOuterAlt(_localctx, 3);
				{
				setState(2473);
				((FrameExtentContext)_localctx).frameType = match(GROUPS);
				setState(2474);
				((FrameExtentContext)_localctx).start = frameBound();
				}
				break;
			case 4:
				enterOuterAlt(_localctx, 4);
				{
				setState(2475);
				((FrameExtentContext)_localctx).frameType = match(RANGE);
				setState(2476);
				match(BETWEEN);
				setState(2477);
				((FrameExtentContext)_localctx).start = frameBound();
				setState(2478);
				match(AND);
				setState(2479);
				((FrameExtentContext)_localctx).end = frameBound();
				}
				break;
			case 5:
				enterOuterAlt(_localctx, 5);
				{
				setState(2481);
				((FrameExtentContext)_localctx).frameType = match(ROWS);
				setState(2482);
				match(BETWEEN);
				setState(2483);
				((FrameExtentContext)_localctx).start = frameBound();
				setState(2484);
				match(AND);
				setState(2485);
				((FrameExtentContext)_localctx).end = frameBound();
				}
				break;
			case 6:
				enterOuterAlt(_localctx, 6);
				{
				setState(2487);
				((FrameExtentContext)_localctx).frameType = match(GROUPS);
				setState(2488);
				match(BETWEEN);
				setState(2489);
				((FrameExtentContext)_localctx).start = frameBound();
				setState(2490);
				match(AND);
				setState(2491);
				((FrameExtentContext)_localctx).end = frameBound();
				}
				break;
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
	public static class FrameBoundContext extends ParserRuleContext {
		public FrameBoundContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_frameBound; }
	 
		public FrameBoundContext() { }
		public void copyFrom(FrameBoundContext ctx) {
			super.copyFrom(ctx);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class BoundedFrameContext extends FrameBoundContext {
		public Token boundType;
		public ExpressionContext expression() {
			return getRuleContext(ExpressionContext.class,0);
		}
		public TerminalNode PRECEDING() { return getToken(SqlBaseParser.PRECEDING, 0); }
		public TerminalNode FOLLOWING() { return getToken(SqlBaseParser.FOLLOWING, 0); }
		public BoundedFrameContext(FrameBoundContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterBoundedFrame(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitBoundedFrame(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitBoundedFrame(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class UnboundedFrameContext extends FrameBoundContext {
		public Token boundType;
		public TerminalNode UNBOUNDED() { return getToken(SqlBaseParser.UNBOUNDED, 0); }
		public TerminalNode PRECEDING() { return getToken(SqlBaseParser.PRECEDING, 0); }
		public TerminalNode FOLLOWING() { return getToken(SqlBaseParser.FOLLOWING, 0); }
		public UnboundedFrameContext(FrameBoundContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterUnboundedFrame(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitUnboundedFrame(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitUnboundedFrame(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class CurrentRowBoundContext extends FrameBoundContext {
		public TerminalNode CURRENT() { return getToken(SqlBaseParser.CURRENT, 0); }
		public TerminalNode ROW() { return getToken(SqlBaseParser.ROW, 0); }
		public CurrentRowBoundContext(FrameBoundContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterCurrentRowBound(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitCurrentRowBound(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitCurrentRowBound(this);
			else return visitor.visitChildren(this);
		}
	}

	public final FrameBoundContext frameBound() throws RecognitionException {
		FrameBoundContext _localctx = new FrameBoundContext(_ctx, getState());
		enterRule(_localctx, 146, RULE_frameBound);
		int _la;
		try {
			setState(2504);
			_errHandler.sync(this);
			switch ( getInterpreter().adaptivePredict(_input,327,_ctx) ) {
			case 1:
				_localctx = new UnboundedFrameContext(_localctx);
				enterOuterAlt(_localctx, 1);
				{
				setState(2495);
				match(UNBOUNDED);
				setState(2496);
				((UnboundedFrameContext)_localctx).boundType = match(PRECEDING);
				}
				break;
			case 2:
				_localctx = new UnboundedFrameContext(_localctx);
				enterOuterAlt(_localctx, 2);
				{
				setState(2497);
				match(UNBOUNDED);
				setState(2498);
				((UnboundedFrameContext)_localctx).boundType = match(FOLLOWING);
				}
				break;
			case 3:
				_localctx = new CurrentRowBoundContext(_localctx);
				enterOuterAlt(_localctx, 3);
				{
				setState(2499);
				match(CURRENT);
				setState(2500);
				match(ROW);
				}
				break;
			case 4:
				_localctx = new BoundedFrameContext(_localctx);
				enterOuterAlt(_localctx, 4);
				{
				setState(2501);
				expression();
				setState(2502);
				((BoundedFrameContext)_localctx).boundType = _input.LT(1);
				_la = _input.LA(1);
				if ( !(_la==FOLLOWING || _la==PRECEDING) ) {
					((BoundedFrameContext)_localctx).boundType = (Token)_errHandler.recoverInline(this);
				}
				else {
					if ( _input.LA(1)==Token.EOF ) matchedEOF = true;
					_errHandler.reportMatch(this);
					consume();
				}
				}
				break;
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
	public static class RowPatternContext extends ParserRuleContext {
		public RowPatternContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_rowPattern; }
	 
		public RowPatternContext() { }
		public void copyFrom(RowPatternContext ctx) {
			super.copyFrom(ctx);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class QuantifiedPrimaryContext extends RowPatternContext {
		public PatternPrimaryContext patternPrimary() {
			return getRuleContext(PatternPrimaryContext.class,0);
		}
		public PatternQuantifierContext patternQuantifier() {
			return getRuleContext(PatternQuantifierContext.class,0);
		}
		public QuantifiedPrimaryContext(RowPatternContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterQuantifiedPrimary(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitQuantifiedPrimary(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitQuantifiedPrimary(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class PatternConcatenationContext extends RowPatternContext {
		public List<RowPatternContext> rowPattern() {
			return getRuleContexts(RowPatternContext.class);
		}
		public RowPatternContext rowPattern(int i) {
			return getRuleContext(RowPatternContext.class,i);
		}
		public PatternConcatenationContext(RowPatternContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterPatternConcatenation(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitPatternConcatenation(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitPatternConcatenation(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class PatternAlternationContext extends RowPatternContext {
		public List<RowPatternContext> rowPattern() {
			return getRuleContexts(RowPatternContext.class);
		}
		public RowPatternContext rowPattern(int i) {
			return getRuleContext(RowPatternContext.class,i);
		}
		public PatternAlternationContext(RowPatternContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterPatternAlternation(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitPatternAlternation(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitPatternAlternation(this);
			else return visitor.visitChildren(this);
		}
	}

	public final RowPatternContext rowPattern() throws RecognitionException {
		return rowPattern(0);
	}

	private RowPatternContext rowPattern(int _p) throws RecognitionException {
		ParserRuleContext _parentctx = _ctx;
		int _parentState = getState();
		RowPatternContext _localctx = new RowPatternContext(_ctx, _parentState);
		RowPatternContext _prevctx = _localctx;
		int _startState = 148;
		enterRecursionRule(_localctx, 148, RULE_rowPattern, _p);
		try {
			int _alt;
			enterOuterAlt(_localctx, 1);
			{
			{
			_localctx = new QuantifiedPrimaryContext(_localctx);
			_ctx = _localctx;
			_prevctx = _localctx;

			setState(2507);
			patternPrimary();
			setState(2509);
			_errHandler.sync(this);
			switch ( getInterpreter().adaptivePredict(_input,328,_ctx) ) {
			case 1:
				{
				setState(2508);
				patternQuantifier();
				}
				break;
			}
			}
			_ctx.stop = _input.LT(-1);
			setState(2518);
			_errHandler.sync(this);
			_alt = getInterpreter().adaptivePredict(_input,330,_ctx);
			while ( _alt!=2 && _alt!=org.antlr.v4.runtime.atn.ATN.INVALID_ALT_NUMBER ) {
				if ( _alt==1 ) {
					if ( _parseListeners!=null ) triggerExitRuleEvent();
					_prevctx = _localctx;
					{
					setState(2516);
					_errHandler.sync(this);
					switch ( getInterpreter().adaptivePredict(_input,329,_ctx) ) {
					case 1:
						{
						_localctx = new PatternConcatenationContext(new RowPatternContext(_parentctx, _parentState));
						pushNewRecursionContext(_localctx, _startState, RULE_rowPattern);
						setState(2511);
						if (!(precpred(_ctx, 2))) throw new FailedPredicateException(this, "precpred(_ctx, 2)");
						setState(2512);
						rowPattern(3);
						}
						break;
					case 2:
						{
						_localctx = new PatternAlternationContext(new RowPatternContext(_parentctx, _parentState));
						pushNewRecursionContext(_localctx, _startState, RULE_rowPattern);
						setState(2513);
						if (!(precpred(_ctx, 1))) throw new FailedPredicateException(this, "precpred(_ctx, 1)");
						setState(2514);
						match(T__13);
						setState(2515);
						rowPattern(2);
						}
						break;
					}
					} 
				}
				setState(2520);
				_errHandler.sync(this);
				_alt = getInterpreter().adaptivePredict(_input,330,_ctx);
			}
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			unrollRecursionContexts(_parentctx);
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class PatternPrimaryContext extends ParserRuleContext {
		public PatternPrimaryContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_patternPrimary; }
	 
		public PatternPrimaryContext() { }
		public void copyFrom(PatternPrimaryContext ctx) {
			super.copyFrom(ctx);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class PatternPermutationContext extends PatternPrimaryContext {
		public TerminalNode PERMUTE() { return getToken(SqlBaseParser.PERMUTE, 0); }
		public List<RowPatternContext> rowPattern() {
			return getRuleContexts(RowPatternContext.class);
		}
		public RowPatternContext rowPattern(int i) {
			return getRuleContext(RowPatternContext.class,i);
		}
		public PatternPermutationContext(PatternPrimaryContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterPatternPermutation(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitPatternPermutation(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitPatternPermutation(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class PartitionEndAnchorContext extends PatternPrimaryContext {
		public PartitionEndAnchorContext(PatternPrimaryContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterPartitionEndAnchor(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitPartitionEndAnchor(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitPartitionEndAnchor(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class PatternVariableContext extends PatternPrimaryContext {
		public IdentifierContext identifier() {
			return getRuleContext(IdentifierContext.class,0);
		}
		public PatternVariableContext(PatternPrimaryContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterPatternVariable(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitPatternVariable(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitPatternVariable(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class ExcludedPatternContext extends PatternPrimaryContext {
		public RowPatternContext rowPattern() {
			return getRuleContext(RowPatternContext.class,0);
		}
		public ExcludedPatternContext(PatternPrimaryContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterExcludedPattern(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitExcludedPattern(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitExcludedPattern(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class PartitionStartAnchorContext extends PatternPrimaryContext {
		public PartitionStartAnchorContext(PatternPrimaryContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterPartitionStartAnchor(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitPartitionStartAnchor(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitPartitionStartAnchor(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class EmptyPatternContext extends PatternPrimaryContext {
		public EmptyPatternContext(PatternPrimaryContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterEmptyPattern(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitEmptyPattern(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitEmptyPattern(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class GroupedPatternContext extends PatternPrimaryContext {
		public RowPatternContext rowPattern() {
			return getRuleContext(RowPatternContext.class,0);
		}
		public GroupedPatternContext(PatternPrimaryContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterGroupedPattern(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitGroupedPattern(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitGroupedPattern(this);
			else return visitor.visitChildren(this);
		}
	}

	public final PatternPrimaryContext patternPrimary() throws RecognitionException {
		PatternPrimaryContext _localctx = new PatternPrimaryContext(_ctx, getState());
		enterRule(_localctx, 150, RULE_patternPrimary);
		int _la;
		try {
			setState(2546);
			_errHandler.sync(this);
			switch ( getInterpreter().adaptivePredict(_input,332,_ctx) ) {
			case 1:
				_localctx = new PatternVariableContext(_localctx);
				enterOuterAlt(_localctx, 1);
				{
				setState(2521);
				identifier();
				}
				break;
			case 2:
				_localctx = new EmptyPatternContext(_localctx);
				enterOuterAlt(_localctx, 2);
				{
				setState(2522);
				match(T__1);
				setState(2523);
				match(T__2);
				}
				break;
			case 3:
				_localctx = new PatternPermutationContext(_localctx);
				enterOuterAlt(_localctx, 3);
				{
				setState(2524);
				match(PERMUTE);
				setState(2525);
				match(T__1);
				setState(2526);
				rowPattern(0);
				setState(2531);
				_errHandler.sync(this);
				_la = _input.LA(1);
				while (_la==T__3) {
					{
					{
					setState(2527);
					match(T__3);
					setState(2528);
					rowPattern(0);
					}
					}
					setState(2533);
					_errHandler.sync(this);
					_la = _input.LA(1);
				}
				setState(2534);
				match(T__2);
				}
				break;
			case 4:
				_localctx = new GroupedPatternContext(_localctx);
				enterOuterAlt(_localctx, 4);
				{
				setState(2536);
				match(T__1);
				setState(2537);
				rowPattern(0);
				setState(2538);
				match(T__2);
				}
				break;
			case 5:
				_localctx = new PartitionStartAnchorContext(_localctx);
				enterOuterAlt(_localctx, 5);
				{
				setState(2540);
				match(T__14);
				}
				break;
			case 6:
				_localctx = new PartitionEndAnchorContext(_localctx);
				enterOuterAlt(_localctx, 6);
				{
				setState(2541);
				match(T__15);
				}
				break;
			case 7:
				_localctx = new ExcludedPatternContext(_localctx);
				enterOuterAlt(_localctx, 7);
				{
				setState(2542);
				match(T__16);
				setState(2543);
				rowPattern(0);
				setState(2544);
				match(T__17);
				}
				break;
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
	public static class PatternQuantifierContext extends ParserRuleContext {
		public PatternQuantifierContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_patternQuantifier; }
	 
		public PatternQuantifierContext() { }
		public void copyFrom(PatternQuantifierContext ctx) {
			super.copyFrom(ctx);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class ZeroOrMoreQuantifierContext extends PatternQuantifierContext {
		public Token reluctant;
		public TerminalNode ASTERISK() { return getToken(SqlBaseParser.ASTERISK, 0); }
		public TerminalNode QUESTION_MARK() { return getToken(SqlBaseParser.QUESTION_MARK, 0); }
		public ZeroOrMoreQuantifierContext(PatternQuantifierContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterZeroOrMoreQuantifier(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitZeroOrMoreQuantifier(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitZeroOrMoreQuantifier(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class OneOrMoreQuantifierContext extends PatternQuantifierContext {
		public Token reluctant;
		public TerminalNode PLUS() { return getToken(SqlBaseParser.PLUS, 0); }
		public TerminalNode QUESTION_MARK() { return getToken(SqlBaseParser.QUESTION_MARK, 0); }
		public OneOrMoreQuantifierContext(PatternQuantifierContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterOneOrMoreQuantifier(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitOneOrMoreQuantifier(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitOneOrMoreQuantifier(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class ZeroOrOneQuantifierContext extends PatternQuantifierContext {
		public Token reluctant;
		public List<TerminalNode> QUESTION_MARK() { return getTokens(SqlBaseParser.QUESTION_MARK); }
		public TerminalNode QUESTION_MARK(int i) {
			return getToken(SqlBaseParser.QUESTION_MARK, i);
		}
		public ZeroOrOneQuantifierContext(PatternQuantifierContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterZeroOrOneQuantifier(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitZeroOrOneQuantifier(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitZeroOrOneQuantifier(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class RangeQuantifierContext extends PatternQuantifierContext {
		public Token exactly;
		public Token reluctant;
		public Token atLeast;
		public Token atMost;
		public List<TerminalNode> INTEGER_VALUE() { return getTokens(SqlBaseParser.INTEGER_VALUE); }
		public TerminalNode INTEGER_VALUE(int i) {
			return getToken(SqlBaseParser.INTEGER_VALUE, i);
		}
		public TerminalNode QUESTION_MARK() { return getToken(SqlBaseParser.QUESTION_MARK, 0); }
		public RangeQuantifierContext(PatternQuantifierContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterRangeQuantifier(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitRangeQuantifier(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitRangeQuantifier(this);
			else return visitor.visitChildren(this);
		}
	}

	public final PatternQuantifierContext patternQuantifier() throws RecognitionException {
		PatternQuantifierContext _localctx = new PatternQuantifierContext(_ctx, getState());
		enterRule(_localctx, 152, RULE_patternQuantifier);
		int _la;
		try {
			setState(2578);
			_errHandler.sync(this);
			switch ( getInterpreter().adaptivePredict(_input,340,_ctx) ) {
			case 1:
				_localctx = new ZeroOrMoreQuantifierContext(_localctx);
				enterOuterAlt(_localctx, 1);
				{
				setState(2548);
				match(ASTERISK);
				setState(2550);
				_errHandler.sync(this);
				switch ( getInterpreter().adaptivePredict(_input,333,_ctx) ) {
				case 1:
					{
					setState(2549);
					((ZeroOrMoreQuantifierContext)_localctx).reluctant = match(QUESTION_MARK);
					}
					break;
				}
				}
				break;
			case 2:
				_localctx = new OneOrMoreQuantifierContext(_localctx);
				enterOuterAlt(_localctx, 2);
				{
				setState(2552);
				match(PLUS);
				setState(2554);
				_errHandler.sync(this);
				switch ( getInterpreter().adaptivePredict(_input,334,_ctx) ) {
				case 1:
					{
					setState(2553);
					((OneOrMoreQuantifierContext)_localctx).reluctant = match(QUESTION_MARK);
					}
					break;
				}
				}
				break;
			case 3:
				_localctx = new ZeroOrOneQuantifierContext(_localctx);
				enterOuterAlt(_localctx, 3);
				{
				setState(2556);
				match(QUESTION_MARK);
				setState(2558);
				_errHandler.sync(this);
				switch ( getInterpreter().adaptivePredict(_input,335,_ctx) ) {
				case 1:
					{
					setState(2557);
					((ZeroOrOneQuantifierContext)_localctx).reluctant = match(QUESTION_MARK);
					}
					break;
				}
				}
				break;
			case 4:
				_localctx = new RangeQuantifierContext(_localctx);
				enterOuterAlt(_localctx, 4);
				{
				setState(2560);
				match(T__18);
				setState(2561);
				((RangeQuantifierContext)_localctx).exactly = match(INTEGER_VALUE);
				setState(2562);
				match(T__19);
				setState(2564);
				_errHandler.sync(this);
				switch ( getInterpreter().adaptivePredict(_input,336,_ctx) ) {
				case 1:
					{
					setState(2563);
					((RangeQuantifierContext)_localctx).reluctant = match(QUESTION_MARK);
					}
					break;
				}
				}
				break;
			case 5:
				_localctx = new RangeQuantifierContext(_localctx);
				enterOuterAlt(_localctx, 5);
				{
				setState(2566);
				match(T__18);
				setState(2568);
				_errHandler.sync(this);
				_la = _input.LA(1);
				if (_la==INTEGER_VALUE) {
					{
					setState(2567);
					((RangeQuantifierContext)_localctx).atLeast = match(INTEGER_VALUE);
					}
				}

				setState(2570);
				match(T__3);
				setState(2572);
				_errHandler.sync(this);
				_la = _input.LA(1);
				if (_la==INTEGER_VALUE) {
					{
					setState(2571);
					((RangeQuantifierContext)_localctx).atMost = match(INTEGER_VALUE);
					}
				}

				setState(2574);
				match(T__19);
				setState(2576);
				_errHandler.sync(this);
				switch ( getInterpreter().adaptivePredict(_input,339,_ctx) ) {
				case 1:
					{
					setState(2575);
					((RangeQuantifierContext)_localctx).reluctant = match(QUESTION_MARK);
					}
					break;
				}
				}
				break;
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
	public static class UpdateAssignmentContext extends ParserRuleContext {
		public IdentifierContext identifier() {
			return getRuleContext(IdentifierContext.class,0);
		}
		public TerminalNode EQ() { return getToken(SqlBaseParser.EQ, 0); }
		public ExpressionContext expression() {
			return getRuleContext(ExpressionContext.class,0);
		}
		public UpdateAssignmentContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_updateAssignment; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterUpdateAssignment(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitUpdateAssignment(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitUpdateAssignment(this);
			else return visitor.visitChildren(this);
		}
	}

	public final UpdateAssignmentContext updateAssignment() throws RecognitionException {
		UpdateAssignmentContext _localctx = new UpdateAssignmentContext(_ctx, getState());
		enterRule(_localctx, 154, RULE_updateAssignment);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(2580);
			identifier();
			setState(2581);
			match(EQ);
			setState(2582);
			expression();
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
	public static class ExplainOptionContext extends ParserRuleContext {
		public ExplainOptionContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_explainOption; }
	 
		public ExplainOptionContext() { }
		public void copyFrom(ExplainOptionContext ctx) {
			super.copyFrom(ctx);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class ExplainFormatContext extends ExplainOptionContext {
		public Token value;
		public TerminalNode FORMAT() { return getToken(SqlBaseParser.FORMAT, 0); }
		public TerminalNode TEXT() { return getToken(SqlBaseParser.TEXT, 0); }
		public TerminalNode GRAPHVIZ() { return getToken(SqlBaseParser.GRAPHVIZ, 0); }
		public TerminalNode JSON() { return getToken(SqlBaseParser.JSON, 0); }
		public ExplainFormatContext(ExplainOptionContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterExplainFormat(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitExplainFormat(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitExplainFormat(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class ExplainTypeContext extends ExplainOptionContext {
		public Token value;
		public TerminalNode TYPE() { return getToken(SqlBaseParser.TYPE, 0); }
		public TerminalNode LOGICAL() { return getToken(SqlBaseParser.LOGICAL, 0); }
		public TerminalNode DISTRIBUTED() { return getToken(SqlBaseParser.DISTRIBUTED, 0); }
		public TerminalNode VALIDATE() { return getToken(SqlBaseParser.VALIDATE, 0); }
		public TerminalNode IO() { return getToken(SqlBaseParser.IO, 0); }
		public ExplainTypeContext(ExplainOptionContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterExplainType(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitExplainType(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitExplainType(this);
			else return visitor.visitChildren(this);
		}
	}

	public final ExplainOptionContext explainOption() throws RecognitionException {
		ExplainOptionContext _localctx = new ExplainOptionContext(_ctx, getState());
		enterRule(_localctx, 156, RULE_explainOption);
		int _la;
		try {
			setState(2588);
			_errHandler.sync(this);
			switch (_input.LA(1)) {
			case FORMAT:
				_localctx = new ExplainFormatContext(_localctx);
				enterOuterAlt(_localctx, 1);
				{
				setState(2584);
				match(FORMAT);
				setState(2585);
				((ExplainFormatContext)_localctx).value = _input.LT(1);
				_la = _input.LA(1);
				if ( !(_la==GRAPHVIZ || _la==JSON || _la==TEXT) ) {
					((ExplainFormatContext)_localctx).value = (Token)_errHandler.recoverInline(this);
				}
				else {
					if ( _input.LA(1)==Token.EOF ) matchedEOF = true;
					_errHandler.reportMatch(this);
					consume();
				}
				}
				break;
			case TYPE:
				_localctx = new ExplainTypeContext(_localctx);
				enterOuterAlt(_localctx, 2);
				{
				setState(2586);
				match(TYPE);
				setState(2587);
				((ExplainTypeContext)_localctx).value = _input.LT(1);
				_la = _input.LA(1);
				if ( !(((((_la - 77)) & ~0x3f) == 0 && ((1L << (_la - 77)) & -9223090561878065151L) != 0) || _la==VALIDATE) ) {
					((ExplainTypeContext)_localctx).value = (Token)_errHandler.recoverInline(this);
				}
				else {
					if ( _input.LA(1)==Token.EOF ) matchedEOF = true;
					_errHandler.reportMatch(this);
					consume();
				}
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
	public static class TransactionModeContext extends ParserRuleContext {
		public TransactionModeContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_transactionMode; }
	 
		public TransactionModeContext() { }
		public void copyFrom(TransactionModeContext ctx) {
			super.copyFrom(ctx);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class TransactionAccessModeContext extends TransactionModeContext {
		public Token accessMode;
		public TerminalNode READ() { return getToken(SqlBaseParser.READ, 0); }
		public TerminalNode ONLY() { return getToken(SqlBaseParser.ONLY, 0); }
		public TerminalNode WRITE() { return getToken(SqlBaseParser.WRITE, 0); }
		public TransactionAccessModeContext(TransactionModeContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterTransactionAccessMode(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitTransactionAccessMode(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitTransactionAccessMode(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class IsolationLevelContext extends TransactionModeContext {
		public TerminalNode ISOLATION() { return getToken(SqlBaseParser.ISOLATION, 0); }
		public TerminalNode LEVEL() { return getToken(SqlBaseParser.LEVEL, 0); }
		public LevelOfIsolationContext levelOfIsolation() {
			return getRuleContext(LevelOfIsolationContext.class,0);
		}
		public IsolationLevelContext(TransactionModeContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterIsolationLevel(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitIsolationLevel(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitIsolationLevel(this);
			else return visitor.visitChildren(this);
		}
	}

	public final TransactionModeContext transactionMode() throws RecognitionException {
		TransactionModeContext _localctx = new TransactionModeContext(_ctx, getState());
		enterRule(_localctx, 158, RULE_transactionMode);
		int _la;
		try {
			setState(2595);
			_errHandler.sync(this);
			switch (_input.LA(1)) {
			case ISOLATION:
				_localctx = new IsolationLevelContext(_localctx);
				enterOuterAlt(_localctx, 1);
				{
				setState(2590);
				match(ISOLATION);
				setState(2591);
				match(LEVEL);
				setState(2592);
				levelOfIsolation();
				}
				break;
			case READ:
				_localctx = new TransactionAccessModeContext(_localctx);
				enterOuterAlt(_localctx, 2);
				{
				setState(2593);
				match(READ);
				setState(2594);
				((TransactionAccessModeContext)_localctx).accessMode = _input.LT(1);
				_la = _input.LA(1);
				if ( !(_la==ONLY || _la==WRITE) ) {
					((TransactionAccessModeContext)_localctx).accessMode = (Token)_errHandler.recoverInline(this);
				}
				else {
					if ( _input.LA(1)==Token.EOF ) matchedEOF = true;
					_errHandler.reportMatch(this);
					consume();
				}
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
	public static class LevelOfIsolationContext extends ParserRuleContext {
		public LevelOfIsolationContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_levelOfIsolation; }
	 
		public LevelOfIsolationContext() { }
		public void copyFrom(LevelOfIsolationContext ctx) {
			super.copyFrom(ctx);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class ReadUncommittedContext extends LevelOfIsolationContext {
		public TerminalNode READ() { return getToken(SqlBaseParser.READ, 0); }
		public TerminalNode UNCOMMITTED() { return getToken(SqlBaseParser.UNCOMMITTED, 0); }
		public ReadUncommittedContext(LevelOfIsolationContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterReadUncommitted(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitReadUncommitted(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitReadUncommitted(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class SerializableContext extends LevelOfIsolationContext {
		public TerminalNode SERIALIZABLE() { return getToken(SqlBaseParser.SERIALIZABLE, 0); }
		public SerializableContext(LevelOfIsolationContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterSerializable(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitSerializable(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitSerializable(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class ReadCommittedContext extends LevelOfIsolationContext {
		public TerminalNode READ() { return getToken(SqlBaseParser.READ, 0); }
		public TerminalNode COMMITTED() { return getToken(SqlBaseParser.COMMITTED, 0); }
		public ReadCommittedContext(LevelOfIsolationContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterReadCommitted(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitReadCommitted(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitReadCommitted(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class RepeatableReadContext extends LevelOfIsolationContext {
		public TerminalNode REPEATABLE() { return getToken(SqlBaseParser.REPEATABLE, 0); }
		public TerminalNode READ() { return getToken(SqlBaseParser.READ, 0); }
		public RepeatableReadContext(LevelOfIsolationContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterRepeatableRead(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitRepeatableRead(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitRepeatableRead(this);
			else return visitor.visitChildren(this);
		}
	}

	public final LevelOfIsolationContext levelOfIsolation() throws RecognitionException {
		LevelOfIsolationContext _localctx = new LevelOfIsolationContext(_ctx, getState());
		enterRule(_localctx, 160, RULE_levelOfIsolation);
		try {
			setState(2604);
			_errHandler.sync(this);
			switch ( getInterpreter().adaptivePredict(_input,343,_ctx) ) {
			case 1:
				_localctx = new ReadUncommittedContext(_localctx);
				enterOuterAlt(_localctx, 1);
				{
				setState(2597);
				match(READ);
				setState(2598);
				match(UNCOMMITTED);
				}
				break;
			case 2:
				_localctx = new ReadCommittedContext(_localctx);
				enterOuterAlt(_localctx, 2);
				{
				setState(2599);
				match(READ);
				setState(2600);
				match(COMMITTED);
				}
				break;
			case 3:
				_localctx = new RepeatableReadContext(_localctx);
				enterOuterAlt(_localctx, 3);
				{
				setState(2601);
				match(REPEATABLE);
				setState(2602);
				match(READ);
				}
				break;
			case 4:
				_localctx = new SerializableContext(_localctx);
				enterOuterAlt(_localctx, 4);
				{
				setState(2603);
				match(SERIALIZABLE);
				}
				break;
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
	public static class CallArgumentContext extends ParserRuleContext {
		public CallArgumentContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_callArgument; }
	 
		public CallArgumentContext() { }
		public void copyFrom(CallArgumentContext ctx) {
			super.copyFrom(ctx);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class PositionalArgumentContext extends CallArgumentContext {
		public ExpressionContext expression() {
			return getRuleContext(ExpressionContext.class,0);
		}
		public PositionalArgumentContext(CallArgumentContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterPositionalArgument(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitPositionalArgument(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitPositionalArgument(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class NamedArgumentContext extends CallArgumentContext {
		public IdentifierContext identifier() {
			return getRuleContext(IdentifierContext.class,0);
		}
		public ExpressionContext expression() {
			return getRuleContext(ExpressionContext.class,0);
		}
		public NamedArgumentContext(CallArgumentContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterNamedArgument(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitNamedArgument(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitNamedArgument(this);
			else return visitor.visitChildren(this);
		}
	}

	public final CallArgumentContext callArgument() throws RecognitionException {
		CallArgumentContext _localctx = new CallArgumentContext(_ctx, getState());
		enterRule(_localctx, 162, RULE_callArgument);
		try {
			setState(2611);
			_errHandler.sync(this);
			switch ( getInterpreter().adaptivePredict(_input,344,_ctx) ) {
			case 1:
				_localctx = new PositionalArgumentContext(_localctx);
				enterOuterAlt(_localctx, 1);
				{
				setState(2606);
				expression();
				}
				break;
			case 2:
				_localctx = new NamedArgumentContext(_localctx);
				enterOuterAlt(_localctx, 2);
				{
				setState(2607);
				identifier();
				setState(2608);
				match(T__20);
				setState(2609);
				expression();
				}
				break;
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
	public static class PathElementContext extends ParserRuleContext {
		public PathElementContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_pathElement; }
	 
		public PathElementContext() { }
		public void copyFrom(PathElementContext ctx) {
			super.copyFrom(ctx);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class QualifiedArgumentContext extends PathElementContext {
		public List<IdentifierContext> identifier() {
			return getRuleContexts(IdentifierContext.class);
		}
		public IdentifierContext identifier(int i) {
			return getRuleContext(IdentifierContext.class,i);
		}
		public QualifiedArgumentContext(PathElementContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterQualifiedArgument(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitQualifiedArgument(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitQualifiedArgument(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class UnqualifiedArgumentContext extends PathElementContext {
		public IdentifierContext identifier() {
			return getRuleContext(IdentifierContext.class,0);
		}
		public UnqualifiedArgumentContext(PathElementContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterUnqualifiedArgument(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitUnqualifiedArgument(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitUnqualifiedArgument(this);
			else return visitor.visitChildren(this);
		}
	}

	public final PathElementContext pathElement() throws RecognitionException {
		PathElementContext _localctx = new PathElementContext(_ctx, getState());
		enterRule(_localctx, 164, RULE_pathElement);
		try {
			setState(2618);
			_errHandler.sync(this);
			switch ( getInterpreter().adaptivePredict(_input,345,_ctx) ) {
			case 1:
				_localctx = new QualifiedArgumentContext(_localctx);
				enterOuterAlt(_localctx, 1);
				{
				setState(2613);
				identifier();
				setState(2614);
				match(T__0);
				setState(2615);
				identifier();
				}
				break;
			case 2:
				_localctx = new UnqualifiedArgumentContext(_localctx);
				enterOuterAlt(_localctx, 2);
				{
				setState(2617);
				identifier();
				}
				break;
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
	public static class PathSpecificationContext extends ParserRuleContext {
		public List<PathElementContext> pathElement() {
			return getRuleContexts(PathElementContext.class);
		}
		public PathElementContext pathElement(int i) {
			return getRuleContext(PathElementContext.class,i);
		}
		public PathSpecificationContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_pathSpecification; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterPathSpecification(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitPathSpecification(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitPathSpecification(this);
			else return visitor.visitChildren(this);
		}
	}

	public final PathSpecificationContext pathSpecification() throws RecognitionException {
		PathSpecificationContext _localctx = new PathSpecificationContext(_ctx, getState());
		enterRule(_localctx, 166, RULE_pathSpecification);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(2620);
			pathElement();
			setState(2625);
			_errHandler.sync(this);
			_la = _input.LA(1);
			while (_la==T__3) {
				{
				{
				setState(2621);
				match(T__3);
				setState(2622);
				pathElement();
				}
				}
				setState(2627);
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
	public static class PrivilegeContext extends ParserRuleContext {
		public TerminalNode CREATE() { return getToken(SqlBaseParser.CREATE, 0); }
		public TerminalNode SELECT() { return getToken(SqlBaseParser.SELECT, 0); }
		public TerminalNode DELETE() { return getToken(SqlBaseParser.DELETE, 0); }
		public TerminalNode INSERT() { return getToken(SqlBaseParser.INSERT, 0); }
		public TerminalNode UPDATE() { return getToken(SqlBaseParser.UPDATE, 0); }
		public PrivilegeContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_privilege; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterPrivilege(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitPrivilege(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitPrivilege(this);
			else return visitor.visitChildren(this);
		}
	}

	public final PrivilegeContext privilege() throws RecognitionException {
		PrivilegeContext _localctx = new PrivilegeContext(_ctx, getState());
		enterRule(_localctx, 168, RULE_privilege);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(2628);
			_la = _input.LA(1);
			if ( !(_la==CREATE || _la==DELETE || _la==INSERT || _la==SELECT || _la==UPDATE) ) {
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

	@SuppressWarnings("CheckReturnValue")
	public static class QualifiedNameContext extends ParserRuleContext {
		public List<IdentifierContext> identifier() {
			return getRuleContexts(IdentifierContext.class);
		}
		public IdentifierContext identifier(int i) {
			return getRuleContext(IdentifierContext.class,i);
		}
		public QualifiedNameContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_qualifiedName; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterQualifiedName(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitQualifiedName(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitQualifiedName(this);
			else return visitor.visitChildren(this);
		}
	}

	public final QualifiedNameContext qualifiedName() throws RecognitionException {
		QualifiedNameContext _localctx = new QualifiedNameContext(_ctx, getState());
		enterRule(_localctx, 170, RULE_qualifiedName);
		try {
			int _alt;
			enterOuterAlt(_localctx, 1);
			{
			setState(2630);
			identifier();
			setState(2635);
			_errHandler.sync(this);
			_alt = getInterpreter().adaptivePredict(_input,347,_ctx);
			while ( _alt!=2 && _alt!=org.antlr.v4.runtime.atn.ATN.INVALID_ALT_NUMBER ) {
				if ( _alt==1 ) {
					{
					{
					setState(2631);
					match(T__0);
					setState(2632);
					identifier();
					}
					} 
				}
				setState(2637);
				_errHandler.sync(this);
				_alt = getInterpreter().adaptivePredict(_input,347,_ctx);
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
	public static class QueryPeriodContext extends ParserRuleContext {
		public ValueExpressionContext end;
		public TerminalNode FOR() { return getToken(SqlBaseParser.FOR, 0); }
		public RangeTypeContext rangeType() {
			return getRuleContext(RangeTypeContext.class,0);
		}
		public TerminalNode AS() { return getToken(SqlBaseParser.AS, 0); }
		public TerminalNode OF() { return getToken(SqlBaseParser.OF, 0); }
		public ValueExpressionContext valueExpression() {
			return getRuleContext(ValueExpressionContext.class,0);
		}
		public QueryPeriodContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_queryPeriod; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterQueryPeriod(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitQueryPeriod(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitQueryPeriod(this);
			else return visitor.visitChildren(this);
		}
	}

	public final QueryPeriodContext queryPeriod() throws RecognitionException {
		QueryPeriodContext _localctx = new QueryPeriodContext(_ctx, getState());
		enterRule(_localctx, 172, RULE_queryPeriod);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(2638);
			match(FOR);
			setState(2639);
			rangeType();
			setState(2640);
			match(AS);
			setState(2641);
			match(OF);
			setState(2642);
			((QueryPeriodContext)_localctx).end = valueExpression(0);
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
	public static class RangeTypeContext extends ParserRuleContext {
		public TerminalNode TIMESTAMP() { return getToken(SqlBaseParser.TIMESTAMP, 0); }
		public TerminalNode VERSION() { return getToken(SqlBaseParser.VERSION, 0); }
		public RangeTypeContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_rangeType; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterRangeType(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitRangeType(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitRangeType(this);
			else return visitor.visitChildren(this);
		}
	}

	public final RangeTypeContext rangeType() throws RecognitionException {
		RangeTypeContext _localctx = new RangeTypeContext(_ctx, getState());
		enterRule(_localctx, 174, RULE_rangeType);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(2644);
			_la = _input.LA(1);
			if ( !(_la==TIMESTAMP || _la==VERSION) ) {
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

	@SuppressWarnings("CheckReturnValue")
	public static class GrantorContext extends ParserRuleContext {
		public GrantorContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_grantor; }
	 
		public GrantorContext() { }
		public void copyFrom(GrantorContext ctx) {
			super.copyFrom(ctx);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class CurrentUserGrantorContext extends GrantorContext {
		public TerminalNode CURRENT_USER() { return getToken(SqlBaseParser.CURRENT_USER, 0); }
		public CurrentUserGrantorContext(GrantorContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterCurrentUserGrantor(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitCurrentUserGrantor(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitCurrentUserGrantor(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class SpecifiedPrincipalContext extends GrantorContext {
		public PrincipalContext principal() {
			return getRuleContext(PrincipalContext.class,0);
		}
		public SpecifiedPrincipalContext(GrantorContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterSpecifiedPrincipal(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitSpecifiedPrincipal(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitSpecifiedPrincipal(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class CurrentRoleGrantorContext extends GrantorContext {
		public TerminalNode CURRENT_ROLE() { return getToken(SqlBaseParser.CURRENT_ROLE, 0); }
		public CurrentRoleGrantorContext(GrantorContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterCurrentRoleGrantor(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitCurrentRoleGrantor(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitCurrentRoleGrantor(this);
			else return visitor.visitChildren(this);
		}
	}

	public final GrantorContext grantor() throws RecognitionException {
		GrantorContext _localctx = new GrantorContext(_ctx, getState());
		enterRule(_localctx, 176, RULE_grantor);
		try {
			setState(2649);
			_errHandler.sync(this);
			switch (_input.LA(1)) {
			case ADD:
			case ADMIN:
			case AFTER:
			case ALL:
			case ANALYZE:
			case ANY:
			case ARRAY:
			case ASC:
			case AT:
			case AUTHORIZATION:
			case BERNOULLI:
			case CALL:
			case CASCADE:
			case CATALOGS:
			case COLLATE:
			case COLUMN:
			case COLUMNS:
			case COMMENT:
			case COMMIT:
			case COMMITTED:
			case COUNT:
			case CURRENT:
			case CURSOR:
			case DATA:
			case DATE:
			case DAY:
			case DECLARE:
			case DEFAULT:
			case DEFINER:
			case DENY:
			case DESC:
			case DEFINE:
			case DISTRIBUTED:
			case DOUBLE:
			case EMPTY:
			case EPOCH:
			case ERROR:
			case EXCLUDING:
			case EXPLAIN:
			case FETCH:
			case FILTER:
			case FINAL:
			case FIRST:
			case FOLLOWING:
			case FORMAT:
			case FUNCTIONS:
			case GRANT:
			case GRANTED:
			case GRANTS:
			case GRAPHVIZ:
			case GROUPS:
			case HOUR:
			case IF:
			case IGNORE:
			case IMPERSONATE:
			case INCLUDING:
			case INITIAL:
			case INPUT:
			case INTERVAL:
			case INVOKER:
			case IO:
			case ISOLATION:
			case JSON:
			case LAST:
			case LATERAL:
			case LEVEL:
			case LIMIT:
			case LOCAL:
			case LOGICAL:
			case MAP:
			case MATCH:
			case MATCHED:
			case MATCHES:
			case MATCH_RECOGNIZE:
			case MATERIALIZED:
			case MEASURES:
			case MERGE:
			case MINUTE:
			case MONTH:
			case NEXT:
			case NFC:
			case NFD:
			case NFKC:
			case NFKD:
			case NO:
			case NONE:
			case NULLIF:
			case NULLS:
			case OFFSET:
			case OMIT:
			case OF:
			case ONE:
			case ONLY:
			case OPERATOR:
			case OPTION:
			case ORDINALITY:
			case OUTPUT:
			case OVER:
			case OVERFLOW:
			case PARTITION:
			case PARTITIONS:
			case PAST:
			case PATH:
			case PATTERN:
			case PER:
			case PERMUTE:
			case POSITION:
			case PRECEDING:
			case PRECISION:
			case PRIVILEGES:
			case PROPERTIES:
			case RANGE:
			case READ:
			case REFRESH:
			case RENAME:
			case REPEATABLE:
			case REPLACE:
			case RESET:
			case RESPECT:
			case RESTRICT:
			case REVOKE:
			case ROLE:
			case ROLES:
			case ROLLBACK:
			case ROW:
			case ROWS:
			case RUNNING:
			case SCHEMA:
			case SCHEMAS:
			case SECOND:
			case SECURITY:
			case SEEK:
			case SERIALIZABLE:
			case SESSION:
			case SESSION_USER:
			case SET:
			case SETS:
			case SHOW:
			case SOME:
			case START:
			case STATS:
			case SUBSET:
			case SUBSTRING:
			case SYSTEM:
			case TABLES:
			case TABLESAMPLE:
			case TEXT:
			case TIES:
			case TIME:
			case TIMESTAMP:
			case TO:
			case TRANSACTION:
			case TRUNCATE:
			case TRY_CAST:
			case TYPE:
			case UNBOUNDED:
			case UNCOMMITTED:
			case UNMATCHED:
			case UPDATE:
			case USE:
			case USER:
			case VALIDATE:
			case VERBOSE:
			case VERSION:
			case VIEW:
			case WINDOW:
			case WITHIN:
			case WITHOUT:
			case WORK:
			case WRITE:
			case YEAR:
			case ZONE:
			case IDENTIFIER:
			case DIGIT_IDENTIFIER:
			case QUOTED_IDENTIFIER:
			case BACKQUOTED_IDENTIFIER:
				_localctx = new SpecifiedPrincipalContext(_localctx);
				enterOuterAlt(_localctx, 1);
				{
				setState(2646);
				principal();
				}
				break;
			case CURRENT_USER:
				_localctx = new CurrentUserGrantorContext(_localctx);
				enterOuterAlt(_localctx, 2);
				{
				setState(2647);
				match(CURRENT_USER);
				}
				break;
			case CURRENT_ROLE:
				_localctx = new CurrentRoleGrantorContext(_localctx);
				enterOuterAlt(_localctx, 3);
				{
				setState(2648);
				match(CURRENT_ROLE);
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
	public static class PrincipalContext extends ParserRuleContext {
		public PrincipalContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_principal; }
	 
		public PrincipalContext() { }
		public void copyFrom(PrincipalContext ctx) {
			super.copyFrom(ctx);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class UnspecifiedPrincipalContext extends PrincipalContext {
		public IdentifierContext identifier() {
			return getRuleContext(IdentifierContext.class,0);
		}
		public UnspecifiedPrincipalContext(PrincipalContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterUnspecifiedPrincipal(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitUnspecifiedPrincipal(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitUnspecifiedPrincipal(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class UserPrincipalContext extends PrincipalContext {
		public TerminalNode USER() { return getToken(SqlBaseParser.USER, 0); }
		public IdentifierContext identifier() {
			return getRuleContext(IdentifierContext.class,0);
		}
		public UserPrincipalContext(PrincipalContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterUserPrincipal(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitUserPrincipal(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitUserPrincipal(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class RolePrincipalContext extends PrincipalContext {
		public TerminalNode ROLE() { return getToken(SqlBaseParser.ROLE, 0); }
		public IdentifierContext identifier() {
			return getRuleContext(IdentifierContext.class,0);
		}
		public RolePrincipalContext(PrincipalContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterRolePrincipal(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitRolePrincipal(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitRolePrincipal(this);
			else return visitor.visitChildren(this);
		}
	}

	public final PrincipalContext principal() throws RecognitionException {
		PrincipalContext _localctx = new PrincipalContext(_ctx, getState());
		enterRule(_localctx, 178, RULE_principal);
		try {
			setState(2656);
			_errHandler.sync(this);
			switch ( getInterpreter().adaptivePredict(_input,349,_ctx) ) {
			case 1:
				_localctx = new UnspecifiedPrincipalContext(_localctx);
				enterOuterAlt(_localctx, 1);
				{
				setState(2651);
				identifier();
				}
				break;
			case 2:
				_localctx = new UserPrincipalContext(_localctx);
				enterOuterAlt(_localctx, 2);
				{
				setState(2652);
				match(USER);
				setState(2653);
				identifier();
				}
				break;
			case 3:
				_localctx = new RolePrincipalContext(_localctx);
				enterOuterAlt(_localctx, 3);
				{
				setState(2654);
				match(ROLE);
				setState(2655);
				identifier();
				}
				break;
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
	public static class RolesContext extends ParserRuleContext {
		public List<IdentifierContext> identifier() {
			return getRuleContexts(IdentifierContext.class);
		}
		public IdentifierContext identifier(int i) {
			return getRuleContext(IdentifierContext.class,i);
		}
		public RolesContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_roles; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterRoles(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitRoles(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitRoles(this);
			else return visitor.visitChildren(this);
		}
	}

	public final RolesContext roles() throws RecognitionException {
		RolesContext _localctx = new RolesContext(_ctx, getState());
		enterRule(_localctx, 180, RULE_roles);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(2658);
			identifier();
			setState(2663);
			_errHandler.sync(this);
			_la = _input.LA(1);
			while (_la==T__3) {
				{
				{
				setState(2659);
				match(T__3);
				setState(2660);
				identifier();
				}
				}
				setState(2665);
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
	public static class IdentifierContext extends ParserRuleContext {
		public IdentifierContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_identifier; }
	 
		public IdentifierContext() { }
		public void copyFrom(IdentifierContext ctx) {
			super.copyFrom(ctx);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class BackQuotedIdentifierContext extends IdentifierContext {
		public TerminalNode BACKQUOTED_IDENTIFIER() { return getToken(SqlBaseParser.BACKQUOTED_IDENTIFIER, 0); }
		public BackQuotedIdentifierContext(IdentifierContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterBackQuotedIdentifier(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitBackQuotedIdentifier(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitBackQuotedIdentifier(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class QuotedIdentifierContext extends IdentifierContext {
		public TerminalNode QUOTED_IDENTIFIER() { return getToken(SqlBaseParser.QUOTED_IDENTIFIER, 0); }
		public QuotedIdentifierContext(IdentifierContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterQuotedIdentifier(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitQuotedIdentifier(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitQuotedIdentifier(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class DigitIdentifierContext extends IdentifierContext {
		public TerminalNode DIGIT_IDENTIFIER() { return getToken(SqlBaseParser.DIGIT_IDENTIFIER, 0); }
		public DigitIdentifierContext(IdentifierContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterDigitIdentifier(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitDigitIdentifier(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitDigitIdentifier(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class UnquotedIdentifierContext extends IdentifierContext {
		public TerminalNode IDENTIFIER() { return getToken(SqlBaseParser.IDENTIFIER, 0); }
		public NonReservedContext nonReserved() {
			return getRuleContext(NonReservedContext.class,0);
		}
		public UnquotedIdentifierContext(IdentifierContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterUnquotedIdentifier(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitUnquotedIdentifier(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitUnquotedIdentifier(this);
			else return visitor.visitChildren(this);
		}
	}

	public final IdentifierContext identifier() throws RecognitionException {
		IdentifierContext _localctx = new IdentifierContext(_ctx, getState());
		enterRule(_localctx, 182, RULE_identifier);
		try {
			setState(2671);
			_errHandler.sync(this);
			switch (_input.LA(1)) {
			case IDENTIFIER:
				_localctx = new UnquotedIdentifierContext(_localctx);
				enterOuterAlt(_localctx, 1);
				{
				setState(2666);
				match(IDENTIFIER);
				}
				break;
			case QUOTED_IDENTIFIER:
				_localctx = new QuotedIdentifierContext(_localctx);
				enterOuterAlt(_localctx, 2);
				{
				setState(2667);
				match(QUOTED_IDENTIFIER);
				}
				break;
			case ADD:
			case ADMIN:
			case AFTER:
			case ALL:
			case ANALYZE:
			case ANY:
			case ARRAY:
			case ASC:
			case AT:
			case AUTHORIZATION:
			case BERNOULLI:
			case CALL:
			case CASCADE:
			case CATALOGS:
			case COLLATE:
			case COLUMN:
			case COLUMNS:
			case COMMENT:
			case COMMIT:
			case COMMITTED:
			case COUNT:
			case CURRENT:
			case CURSOR:
			case DATA:
			case DATE:
			case DAY:
			case DECLARE:
			case DEFAULT:
			case DEFINER:
			case DENY:
			case DESC:
			case DEFINE:
			case DISTRIBUTED:
			case DOUBLE:
			case EMPTY:
			case EPOCH:
			case ERROR:
			case EXCLUDING:
			case EXPLAIN:
			case FETCH:
			case FILTER:
			case FINAL:
			case FIRST:
			case FOLLOWING:
			case FORMAT:
			case FUNCTIONS:
			case GRANT:
			case GRANTED:
			case GRANTS:
			case GRAPHVIZ:
			case GROUPS:
			case HOUR:
			case IF:
			case IGNORE:
			case IMPERSONATE:
			case INCLUDING:
			case INITIAL:
			case INPUT:
			case INTERVAL:
			case INVOKER:
			case IO:
			case ISOLATION:
			case JSON:
			case LAST:
			case LATERAL:
			case LEVEL:
			case LIMIT:
			case LOCAL:
			case LOGICAL:
			case MAP:
			case MATCH:
			case MATCHED:
			case MATCHES:
			case MATCH_RECOGNIZE:
			case MATERIALIZED:
			case MEASURES:
			case MERGE:
			case MINUTE:
			case MONTH:
			case NEXT:
			case NFC:
			case NFD:
			case NFKC:
			case NFKD:
			case NO:
			case NONE:
			case NULLIF:
			case NULLS:
			case OFFSET:
			case OMIT:
			case OF:
			case ONE:
			case ONLY:
			case OPERATOR:
			case OPTION:
			case ORDINALITY:
			case OUTPUT:
			case OVER:
			case OVERFLOW:
			case PARTITION:
			case PARTITIONS:
			case PAST:
			case PATH:
			case PATTERN:
			case PER:
			case PERMUTE:
			case POSITION:
			case PRECEDING:
			case PRECISION:
			case PRIVILEGES:
			case PROPERTIES:
			case RANGE:
			case READ:
			case REFRESH:
			case RENAME:
			case REPEATABLE:
			case REPLACE:
			case RESET:
			case RESPECT:
			case RESTRICT:
			case REVOKE:
			case ROLE:
			case ROLES:
			case ROLLBACK:
			case ROW:
			case ROWS:
			case RUNNING:
			case SCHEMA:
			case SCHEMAS:
			case SECOND:
			case SECURITY:
			case SEEK:
			case SERIALIZABLE:
			case SESSION:
			case SESSION_USER:
			case SET:
			case SETS:
			case SHOW:
			case SOME:
			case START:
			case STATS:
			case SUBSET:
			case SUBSTRING:
			case SYSTEM:
			case TABLES:
			case TABLESAMPLE:
			case TEXT:
			case TIES:
			case TIME:
			case TIMESTAMP:
			case TO:
			case TRANSACTION:
			case TRUNCATE:
			case TRY_CAST:
			case TYPE:
			case UNBOUNDED:
			case UNCOMMITTED:
			case UNMATCHED:
			case UPDATE:
			case USE:
			case USER:
			case VALIDATE:
			case VERBOSE:
			case VERSION:
			case VIEW:
			case WINDOW:
			case WITHIN:
			case WITHOUT:
			case WORK:
			case WRITE:
			case YEAR:
			case ZONE:
				_localctx = new UnquotedIdentifierContext(_localctx);
				enterOuterAlt(_localctx, 3);
				{
				setState(2668);
				nonReserved();
				}
				break;
			case BACKQUOTED_IDENTIFIER:
				_localctx = new BackQuotedIdentifierContext(_localctx);
				enterOuterAlt(_localctx, 4);
				{
				setState(2669);
				match(BACKQUOTED_IDENTIFIER);
				}
				break;
			case DIGIT_IDENTIFIER:
				_localctx = new DigitIdentifierContext(_localctx);
				enterOuterAlt(_localctx, 5);
				{
				setState(2670);
				match(DIGIT_IDENTIFIER);
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
	public static class NumberContext extends ParserRuleContext {
		public NumberContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_number; }
	 
		public NumberContext() { }
		public void copyFrom(NumberContext ctx) {
			super.copyFrom(ctx);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class DecimalLiteralContext extends NumberContext {
		public TerminalNode DECIMAL_VALUE() { return getToken(SqlBaseParser.DECIMAL_VALUE, 0); }
		public TerminalNode MINUS() { return getToken(SqlBaseParser.MINUS, 0); }
		public DecimalLiteralContext(NumberContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterDecimalLiteral(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitDecimalLiteral(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitDecimalLiteral(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class DoubleLiteralContext extends NumberContext {
		public TerminalNode DOUBLE_VALUE() { return getToken(SqlBaseParser.DOUBLE_VALUE, 0); }
		public TerminalNode MINUS() { return getToken(SqlBaseParser.MINUS, 0); }
		public DoubleLiteralContext(NumberContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterDoubleLiteral(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitDoubleLiteral(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitDoubleLiteral(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class IntegerLiteralContext extends NumberContext {
		public TerminalNode INTEGER_VALUE() { return getToken(SqlBaseParser.INTEGER_VALUE, 0); }
		public TerminalNode MINUS() { return getToken(SqlBaseParser.MINUS, 0); }
		public IntegerLiteralContext(NumberContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterIntegerLiteral(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitIntegerLiteral(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitIntegerLiteral(this);
			else return visitor.visitChildren(this);
		}
	}

	public final NumberContext number() throws RecognitionException {
		NumberContext _localctx = new NumberContext(_ctx, getState());
		enterRule(_localctx, 184, RULE_number);
		int _la;
		try {
			setState(2685);
			_errHandler.sync(this);
			switch ( getInterpreter().adaptivePredict(_input,355,_ctx) ) {
			case 1:
				_localctx = new DecimalLiteralContext(_localctx);
				enterOuterAlt(_localctx, 1);
				{
				setState(2674);
				_errHandler.sync(this);
				_la = _input.LA(1);
				if (_la==MINUS) {
					{
					setState(2673);
					match(MINUS);
					}
				}

				setState(2676);
				match(DECIMAL_VALUE);
				}
				break;
			case 2:
				_localctx = new DoubleLiteralContext(_localctx);
				enterOuterAlt(_localctx, 2);
				{
				setState(2678);
				_errHandler.sync(this);
				_la = _input.LA(1);
				if (_la==MINUS) {
					{
					setState(2677);
					match(MINUS);
					}
				}

				setState(2680);
				match(DOUBLE_VALUE);
				}
				break;
			case 3:
				_localctx = new IntegerLiteralContext(_localctx);
				enterOuterAlt(_localctx, 3);
				{
				setState(2682);
				_errHandler.sync(this);
				_la = _input.LA(1);
				if (_la==MINUS) {
					{
					setState(2681);
					match(MINUS);
					}
				}

				setState(2684);
				match(INTEGER_VALUE);
				}
				break;
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
	public static class QuotedRegexMatchContext extends ParserRuleContext {
		public TerminalNode OPERATOR() { return getToken(SqlBaseParser.OPERATOR, 0); }
		public TerminalNode REGEX_MATCH() { return getToken(SqlBaseParser.REGEX_MATCH, 0); }
		public TerminalNode IDENTIFIER() { return getToken(SqlBaseParser.IDENTIFIER, 0); }
		public QuotedRegexMatchContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_quotedRegexMatch; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterQuotedRegexMatch(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitQuotedRegexMatch(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitQuotedRegexMatch(this);
			else return visitor.visitChildren(this);
		}
	}

	public final QuotedRegexMatchContext quotedRegexMatch() throws RecognitionException {
		QuotedRegexMatchContext _localctx = new QuotedRegexMatchContext(_ctx, getState());
		enterRule(_localctx, 186, RULE_quotedRegexMatch);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(2687);
			match(OPERATOR);
			setState(2688);
			match(T__1);
			setState(2691);
			_errHandler.sync(this);
			_la = _input.LA(1);
			if (_la==IDENTIFIER) {
				{
				setState(2689);
				match(IDENTIFIER);
				setState(2690);
				match(T__0);
				}
			}

			setState(2693);
			match(REGEX_MATCH);
			setState(2694);
			match(T__2);
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
	public static class CollateClauseContext extends ParserRuleContext {
		public TerminalNode COLLATE() { return getToken(SqlBaseParser.COLLATE, 0); }
		public List<TerminalNode> IDENTIFIER() { return getTokens(SqlBaseParser.IDENTIFIER); }
		public TerminalNode IDENTIFIER(int i) {
			return getToken(SqlBaseParser.IDENTIFIER, i);
		}
		public List<TerminalNode> QUOTED_IDENTIFIER() { return getTokens(SqlBaseParser.QUOTED_IDENTIFIER); }
		public TerminalNode QUOTED_IDENTIFIER(int i) {
			return getToken(SqlBaseParser.QUOTED_IDENTIFIER, i);
		}
		public TerminalNode DEFAULT() { return getToken(SqlBaseParser.DEFAULT, 0); }
		public CollateClauseContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_collateClause; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterCollateClause(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitCollateClause(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitCollateClause(this);
			else return visitor.visitChildren(this);
		}
	}

	public final CollateClauseContext collateClause() throws RecognitionException {
		CollateClauseContext _localctx = new CollateClauseContext(_ctx, getState());
		enterRule(_localctx, 188, RULE_collateClause);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(2696);
			match(COLLATE);
			setState(2699);
			_errHandler.sync(this);
			switch ( getInterpreter().adaptivePredict(_input,357,_ctx) ) {
			case 1:
				{
				setState(2697);
				_la = _input.LA(1);
				if ( !(_la==IDENTIFIER || _la==QUOTED_IDENTIFIER) ) {
				_errHandler.recoverInline(this);
				}
				else {
					if ( _input.LA(1)==Token.EOF ) matchedEOF = true;
					_errHandler.reportMatch(this);
					consume();
				}
				setState(2698);
				match(T__0);
				}
				break;
			}
			setState(2701);
			_la = _input.LA(1);
			if ( !(_la==DEFAULT || _la==IDENTIFIER || _la==QUOTED_IDENTIFIER) ) {
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

	@SuppressWarnings("CheckReturnValue")
	public static class NonReservedContext extends ParserRuleContext {
		public TerminalNode ADD() { return getToken(SqlBaseParser.ADD, 0); }
		public TerminalNode ADMIN() { return getToken(SqlBaseParser.ADMIN, 0); }
		public TerminalNode AFTER() { return getToken(SqlBaseParser.AFTER, 0); }
		public TerminalNode ALL() { return getToken(SqlBaseParser.ALL, 0); }
		public TerminalNode ANALYZE() { return getToken(SqlBaseParser.ANALYZE, 0); }
		public TerminalNode ANY() { return getToken(SqlBaseParser.ANY, 0); }
		public TerminalNode ARRAY() { return getToken(SqlBaseParser.ARRAY, 0); }
		public TerminalNode ASC() { return getToken(SqlBaseParser.ASC, 0); }
		public TerminalNode AT() { return getToken(SqlBaseParser.AT, 0); }
		public TerminalNode AUTHORIZATION() { return getToken(SqlBaseParser.AUTHORIZATION, 0); }
		public TerminalNode BERNOULLI() { return getToken(SqlBaseParser.BERNOULLI, 0); }
		public TerminalNode CALL() { return getToken(SqlBaseParser.CALL, 0); }
		public TerminalNode CASCADE() { return getToken(SqlBaseParser.CASCADE, 0); }
		public TerminalNode CATALOGS() { return getToken(SqlBaseParser.CATALOGS, 0); }
		public TerminalNode COLUMN() { return getToken(SqlBaseParser.COLUMN, 0); }
		public TerminalNode COLUMNS() { return getToken(SqlBaseParser.COLUMNS, 0); }
		public TerminalNode COMMENT() { return getToken(SqlBaseParser.COMMENT, 0); }
		public TerminalNode COMMIT() { return getToken(SqlBaseParser.COMMIT, 0); }
		public TerminalNode COMMITTED() { return getToken(SqlBaseParser.COMMITTED, 0); }
		public TerminalNode COUNT() { return getToken(SqlBaseParser.COUNT, 0); }
		public TerminalNode CURRENT() { return getToken(SqlBaseParser.CURRENT, 0); }
		public TerminalNode COLLATE() { return getToken(SqlBaseParser.COLLATE, 0); }
		public TerminalNode CURSOR() { return getToken(SqlBaseParser.CURSOR, 0); }
		public TerminalNode DATA() { return getToken(SqlBaseParser.DATA, 0); }
		public TerminalNode DATE() { return getToken(SqlBaseParser.DATE, 0); }
		public TerminalNode DAY() { return getToken(SqlBaseParser.DAY, 0); }
		public TerminalNode DEFAULT() { return getToken(SqlBaseParser.DEFAULT, 0); }
		public TerminalNode DEFINE() { return getToken(SqlBaseParser.DEFINE, 0); }
		public TerminalNode DEFINER() { return getToken(SqlBaseParser.DEFINER, 0); }
		public TerminalNode DESC() { return getToken(SqlBaseParser.DESC, 0); }
		public TerminalNode DISTRIBUTED() { return getToken(SqlBaseParser.DISTRIBUTED, 0); }
		public TerminalNode DOUBLE() { return getToken(SqlBaseParser.DOUBLE, 0); }
		public TerminalNode DECLARE() { return getToken(SqlBaseParser.DECLARE, 0); }
		public TerminalNode EMPTY() { return getToken(SqlBaseParser.EMPTY, 0); }
		public TerminalNode ERROR() { return getToken(SqlBaseParser.ERROR, 0); }
		public TerminalNode EXCLUDING() { return getToken(SqlBaseParser.EXCLUDING, 0); }
		public TerminalNode EXPLAIN() { return getToken(SqlBaseParser.EXPLAIN, 0); }
		public TerminalNode EPOCH() { return getToken(SqlBaseParser.EPOCH, 0); }
		public TerminalNode FETCH() { return getToken(SqlBaseParser.FETCH, 0); }
		public TerminalNode FILTER() { return getToken(SqlBaseParser.FILTER, 0); }
		public TerminalNode FINAL() { return getToken(SqlBaseParser.FINAL, 0); }
		public TerminalNode FIRST() { return getToken(SqlBaseParser.FIRST, 0); }
		public TerminalNode FOLLOWING() { return getToken(SqlBaseParser.FOLLOWING, 0); }
		public TerminalNode FORMAT() { return getToken(SqlBaseParser.FORMAT, 0); }
		public TerminalNode FUNCTIONS() { return getToken(SqlBaseParser.FUNCTIONS, 0); }
		public TerminalNode GRANT() { return getToken(SqlBaseParser.GRANT, 0); }
		public TerminalNode DENY() { return getToken(SqlBaseParser.DENY, 0); }
		public TerminalNode GRANTED() { return getToken(SqlBaseParser.GRANTED, 0); }
		public TerminalNode GRANTS() { return getToken(SqlBaseParser.GRANTS, 0); }
		public TerminalNode GRAPHVIZ() { return getToken(SqlBaseParser.GRAPHVIZ, 0); }
		public TerminalNode GROUPS() { return getToken(SqlBaseParser.GROUPS, 0); }
		public TerminalNode HOUR() { return getToken(SqlBaseParser.HOUR, 0); }
		public TerminalNode IF() { return getToken(SqlBaseParser.IF, 0); }
		public TerminalNode IGNORE() { return getToken(SqlBaseParser.IGNORE, 0); }
		public TerminalNode INCLUDING() { return getToken(SqlBaseParser.INCLUDING, 0); }
		public TerminalNode INITIAL() { return getToken(SqlBaseParser.INITIAL, 0); }
		public TerminalNode INPUT() { return getToken(SqlBaseParser.INPUT, 0); }
		public TerminalNode INTERVAL() { return getToken(SqlBaseParser.INTERVAL, 0); }
		public TerminalNode INVOKER() { return getToken(SqlBaseParser.INVOKER, 0); }
		public TerminalNode IO() { return getToken(SqlBaseParser.IO, 0); }
		public TerminalNode ISOLATION() { return getToken(SqlBaseParser.ISOLATION, 0); }
		public TerminalNode IMPERSONATE() { return getToken(SqlBaseParser.IMPERSONATE, 0); }
		public TerminalNode JSON() { return getToken(SqlBaseParser.JSON, 0); }
		public TerminalNode LAST() { return getToken(SqlBaseParser.LAST, 0); }
		public TerminalNode LATERAL() { return getToken(SqlBaseParser.LATERAL, 0); }
		public TerminalNode LEVEL() { return getToken(SqlBaseParser.LEVEL, 0); }
		public TerminalNode LIMIT() { return getToken(SqlBaseParser.LIMIT, 0); }
		public TerminalNode LOCAL() { return getToken(SqlBaseParser.LOCAL, 0); }
		public TerminalNode LOGICAL() { return getToken(SqlBaseParser.LOGICAL, 0); }
		public TerminalNode MAP() { return getToken(SqlBaseParser.MAP, 0); }
		public TerminalNode MATCH() { return getToken(SqlBaseParser.MATCH, 0); }
		public TerminalNode MATCHED() { return getToken(SqlBaseParser.MATCHED, 0); }
		public TerminalNode MATCHES() { return getToken(SqlBaseParser.MATCHES, 0); }
		public TerminalNode MATCH_RECOGNIZE() { return getToken(SqlBaseParser.MATCH_RECOGNIZE, 0); }
		public TerminalNode MATERIALIZED() { return getToken(SqlBaseParser.MATERIALIZED, 0); }
		public TerminalNode MEASURES() { return getToken(SqlBaseParser.MEASURES, 0); }
		public TerminalNode MERGE() { return getToken(SqlBaseParser.MERGE, 0); }
		public TerminalNode MINUTE() { return getToken(SqlBaseParser.MINUTE, 0); }
		public TerminalNode MONTH() { return getToken(SqlBaseParser.MONTH, 0); }
		public TerminalNode NEXT() { return getToken(SqlBaseParser.NEXT, 0); }
		public TerminalNode NFC() { return getToken(SqlBaseParser.NFC, 0); }
		public TerminalNode NFD() { return getToken(SqlBaseParser.NFD, 0); }
		public TerminalNode NFKC() { return getToken(SqlBaseParser.NFKC, 0); }
		public TerminalNode NFKD() { return getToken(SqlBaseParser.NFKD, 0); }
		public TerminalNode NO() { return getToken(SqlBaseParser.NO, 0); }
		public TerminalNode NONE() { return getToken(SqlBaseParser.NONE, 0); }
		public TerminalNode NULLIF() { return getToken(SqlBaseParser.NULLIF, 0); }
		public TerminalNode NULLS() { return getToken(SqlBaseParser.NULLS, 0); }
		public TerminalNode OF() { return getToken(SqlBaseParser.OF, 0); }
		public TerminalNode OFFSET() { return getToken(SqlBaseParser.OFFSET, 0); }
		public TerminalNode OMIT() { return getToken(SqlBaseParser.OMIT, 0); }
		public TerminalNode ONE() { return getToken(SqlBaseParser.ONE, 0); }
		public TerminalNode ONLY() { return getToken(SqlBaseParser.ONLY, 0); }
		public TerminalNode OPTION() { return getToken(SqlBaseParser.OPTION, 0); }
		public TerminalNode ORDINALITY() { return getToken(SqlBaseParser.ORDINALITY, 0); }
		public TerminalNode OUTPUT() { return getToken(SqlBaseParser.OUTPUT, 0); }
		public TerminalNode OVER() { return getToken(SqlBaseParser.OVER, 0); }
		public TerminalNode OVERFLOW() { return getToken(SqlBaseParser.OVERFLOW, 0); }
		public TerminalNode OPERATOR() { return getToken(SqlBaseParser.OPERATOR, 0); }
		public TerminalNode PARTITION() { return getToken(SqlBaseParser.PARTITION, 0); }
		public TerminalNode PARTITIONS() { return getToken(SqlBaseParser.PARTITIONS, 0); }
		public TerminalNode PAST() { return getToken(SqlBaseParser.PAST, 0); }
		public TerminalNode PATH() { return getToken(SqlBaseParser.PATH, 0); }
		public TerminalNode PATTERN() { return getToken(SqlBaseParser.PATTERN, 0); }
		public TerminalNode PER() { return getToken(SqlBaseParser.PER, 0); }
		public TerminalNode PERMUTE() { return getToken(SqlBaseParser.PERMUTE, 0); }
		public TerminalNode POSITION() { return getToken(SqlBaseParser.POSITION, 0); }
		public TerminalNode PRECEDING() { return getToken(SqlBaseParser.PRECEDING, 0); }
		public TerminalNode PRECISION() { return getToken(SqlBaseParser.PRECISION, 0); }
		public TerminalNode PRIVILEGES() { return getToken(SqlBaseParser.PRIVILEGES, 0); }
		public TerminalNode PROPERTIES() { return getToken(SqlBaseParser.PROPERTIES, 0); }
		public TerminalNode RANGE() { return getToken(SqlBaseParser.RANGE, 0); }
		public TerminalNode READ() { return getToken(SqlBaseParser.READ, 0); }
		public TerminalNode REFRESH() { return getToken(SqlBaseParser.REFRESH, 0); }
		public TerminalNode RENAME() { return getToken(SqlBaseParser.RENAME, 0); }
		public TerminalNode REPEATABLE() { return getToken(SqlBaseParser.REPEATABLE, 0); }
		public TerminalNode REPLACE() { return getToken(SqlBaseParser.REPLACE, 0); }
		public TerminalNode RESET() { return getToken(SqlBaseParser.RESET, 0); }
		public TerminalNode RESPECT() { return getToken(SqlBaseParser.RESPECT, 0); }
		public TerminalNode RESTRICT() { return getToken(SqlBaseParser.RESTRICT, 0); }
		public TerminalNode REVOKE() { return getToken(SqlBaseParser.REVOKE, 0); }
		public TerminalNode ROLE() { return getToken(SqlBaseParser.ROLE, 0); }
		public TerminalNode ROLES() { return getToken(SqlBaseParser.ROLES, 0); }
		public TerminalNode ROLLBACK() { return getToken(SqlBaseParser.ROLLBACK, 0); }
		public TerminalNode ROW() { return getToken(SqlBaseParser.ROW, 0); }
		public TerminalNode ROWS() { return getToken(SqlBaseParser.ROWS, 0); }
		public TerminalNode RUNNING() { return getToken(SqlBaseParser.RUNNING, 0); }
		public TerminalNode SCHEMA() { return getToken(SqlBaseParser.SCHEMA, 0); }
		public TerminalNode SCHEMAS() { return getToken(SqlBaseParser.SCHEMAS, 0); }
		public TerminalNode SECOND() { return getToken(SqlBaseParser.SECOND, 0); }
		public TerminalNode SECURITY() { return getToken(SqlBaseParser.SECURITY, 0); }
		public TerminalNode SEEK() { return getToken(SqlBaseParser.SEEK, 0); }
		public TerminalNode SERIALIZABLE() { return getToken(SqlBaseParser.SERIALIZABLE, 0); }
		public TerminalNode SESSION() { return getToken(SqlBaseParser.SESSION, 0); }
		public TerminalNode SET() { return getToken(SqlBaseParser.SET, 0); }
		public TerminalNode SETS() { return getToken(SqlBaseParser.SETS, 0); }
		public TerminalNode SHOW() { return getToken(SqlBaseParser.SHOW, 0); }
		public TerminalNode SOME() { return getToken(SqlBaseParser.SOME, 0); }
		public TerminalNode START() { return getToken(SqlBaseParser.START, 0); }
		public TerminalNode STATS() { return getToken(SqlBaseParser.STATS, 0); }
		public TerminalNode SUBSET() { return getToken(SqlBaseParser.SUBSET, 0); }
		public TerminalNode SUBSTRING() { return getToken(SqlBaseParser.SUBSTRING, 0); }
		public TerminalNode SYSTEM() { return getToken(SqlBaseParser.SYSTEM, 0); }
		public TerminalNode TABLES() { return getToken(SqlBaseParser.TABLES, 0); }
		public TerminalNode TABLESAMPLE() { return getToken(SqlBaseParser.TABLESAMPLE, 0); }
		public TerminalNode TEXT() { return getToken(SqlBaseParser.TEXT, 0); }
		public TerminalNode TIES() { return getToken(SqlBaseParser.TIES, 0); }
		public TerminalNode TIME() { return getToken(SqlBaseParser.TIME, 0); }
		public TerminalNode TIMESTAMP() { return getToken(SqlBaseParser.TIMESTAMP, 0); }
		public TerminalNode TO() { return getToken(SqlBaseParser.TO, 0); }
		public TerminalNode TRANSACTION() { return getToken(SqlBaseParser.TRANSACTION, 0); }
		public TerminalNode TRUNCATE() { return getToken(SqlBaseParser.TRUNCATE, 0); }
		public TerminalNode TRY_CAST() { return getToken(SqlBaseParser.TRY_CAST, 0); }
		public TerminalNode TYPE() { return getToken(SqlBaseParser.TYPE, 0); }
		public TerminalNode UNBOUNDED() { return getToken(SqlBaseParser.UNBOUNDED, 0); }
		public TerminalNode UNCOMMITTED() { return getToken(SqlBaseParser.UNCOMMITTED, 0); }
		public TerminalNode UNMATCHED() { return getToken(SqlBaseParser.UNMATCHED, 0); }
		public TerminalNode UPDATE() { return getToken(SqlBaseParser.UPDATE, 0); }
		public TerminalNode USE() { return getToken(SqlBaseParser.USE, 0); }
		public TerminalNode USER() { return getToken(SqlBaseParser.USER, 0); }
		public TerminalNode SESSION_USER() { return getToken(SqlBaseParser.SESSION_USER, 0); }
		public TerminalNode VALIDATE() { return getToken(SqlBaseParser.VALIDATE, 0); }
		public TerminalNode VERBOSE() { return getToken(SqlBaseParser.VERBOSE, 0); }
		public TerminalNode VERSION() { return getToken(SqlBaseParser.VERSION, 0); }
		public TerminalNode VIEW() { return getToken(SqlBaseParser.VIEW, 0); }
		public TerminalNode WINDOW() { return getToken(SqlBaseParser.WINDOW, 0); }
		public TerminalNode WITHIN() { return getToken(SqlBaseParser.WITHIN, 0); }
		public TerminalNode WITHOUT() { return getToken(SqlBaseParser.WITHOUT, 0); }
		public TerminalNode WORK() { return getToken(SqlBaseParser.WORK, 0); }
		public TerminalNode WRITE() { return getToken(SqlBaseParser.WRITE, 0); }
		public TerminalNode YEAR() { return getToken(SqlBaseParser.YEAR, 0); }
		public TerminalNode ZONE() { return getToken(SqlBaseParser.ZONE, 0); }
		public NonReservedContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_nonReserved; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).enterNonReserved(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof SqlBaseListener ) ((SqlBaseListener)listener).exitNonReserved(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof SqlBaseVisitor ) return ((SqlBaseVisitor<? extends T>)visitor).visitNonReserved(this);
			else return visitor.visitChildren(this);
		}
	}

	public final NonReservedContext nonReserved() throws RecognitionException {
		NonReservedContext _localctx = new NonReservedContext(_ctx, getState());
		enterRule(_localctx, 190, RULE_nonReserved);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(2703);
			_la = _input.LA(1);
			if ( !(((((_la - 22)) & ~0x3f) == 0 && ((1L << (_la - 22)) & 7614986641231527343L) != 0) || ((((_la - 87)) & ~0x3f) == 0 && ((1L << (_la - 87)) & -7497116950751287L) != 0) || ((((_la - 152)) & ~0x3f) == 0 && ((1L << (_la - 152)) & -38285132329681793L) != 0) || ((((_la - 217)) & ~0x3f) == 0 && ((1L << (_la - 217)) & 2227436003454975L) != 0)) ) {
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

	public boolean sempred(RuleContext _localctx, int ruleIndex, int predIndex) {
		switch (ruleIndex) {
		case 19:
			return queryTerm_sempred((QueryTermContext)_localctx, predIndex);
		case 31:
			return relation_sempred((RelationContext)_localctx, predIndex);
		case 49:
			return booleanExpression_sempred((BooleanExpressionContext)_localctx, predIndex);
		case 52:
			return valueExpression_sempred((ValueExpressionContext)_localctx, predIndex);
		case 53:
			return primaryExpression_sempred((PrimaryExpressionContext)_localctx, predIndex);
		case 64:
			return type_sempred((TypeContext)_localctx, predIndex);
		case 74:
			return rowPattern_sempred((RowPatternContext)_localctx, predIndex);
		}
		return true;
	}
	private boolean queryTerm_sempred(QueryTermContext _localctx, int predIndex) {
		switch (predIndex) {
		case 0:
			return precpred(_ctx, 2);
		case 1:
			return precpred(_ctx, 1);
		}
		return true;
	}
	private boolean relation_sempred(RelationContext _localctx, int predIndex) {
		switch (predIndex) {
		case 2:
			return precpred(_ctx, 2);
		}
		return true;
	}
	private boolean booleanExpression_sempred(BooleanExpressionContext _localctx, int predIndex) {
		switch (predIndex) {
		case 3:
			return precpred(_ctx, 2);
		case 4:
			return precpred(_ctx, 1);
		}
		return true;
	}
	private boolean valueExpression_sempred(ValueExpressionContext _localctx, int predIndex) {
		switch (predIndex) {
		case 5:
			return precpred(_ctx, 4);
		case 6:
			return precpred(_ctx, 3);
		case 7:
			return precpred(_ctx, 2);
		case 8:
			return precpred(_ctx, 1);
		case 9:
			return precpred(_ctx, 6);
		}
		return true;
	}
	private boolean primaryExpression_sempred(PrimaryExpressionContext _localctx, int predIndex) {
		switch (predIndex) {
		case 10:
			return precpred(_ctx, 20);
		case 11:
			return precpred(_ctx, 17);
		case 12:
			return precpred(_ctx, 15);
		}
		return true;
	}
	private boolean type_sempred(TypeContext _localctx, int predIndex) {
		switch (predIndex) {
		case 13:
			return precpred(_ctx, 2);
		}
		return true;
	}
	private boolean rowPattern_sempred(RowPatternContext _localctx, int predIndex) {
		switch (predIndex) {
		case 14:
			return precpred(_ctx, 2);
		case 15:
			return precpred(_ctx, 1);
		}
		return true;
	}

	private static final String _serializedATNSegment0 =
		"\u0004\u0001\u012a\u0a92\u0002\u0000\u0007\u0000\u0002\u0001\u0007\u0001"+
		"\u0002\u0002\u0007\u0002\u0002\u0003\u0007\u0003\u0002\u0004\u0007\u0004"+
		"\u0002\u0005\u0007\u0005\u0002\u0006\u0007\u0006\u0002\u0007\u0007\u0007"+
		"\u0002\b\u0007\b\u0002\t\u0007\t\u0002\n\u0007\n\u0002\u000b\u0007\u000b"+
		"\u0002\f\u0007\f\u0002\r\u0007\r\u0002\u000e\u0007\u000e\u0002\u000f\u0007"+
		"\u000f\u0002\u0010\u0007\u0010\u0002\u0011\u0007\u0011\u0002\u0012\u0007"+
		"\u0012\u0002\u0013\u0007\u0013\u0002\u0014\u0007\u0014\u0002\u0015\u0007"+
		"\u0015\u0002\u0016\u0007\u0016\u0002\u0017\u0007\u0017\u0002\u0018\u0007"+
		"\u0018\u0002\u0019\u0007\u0019\u0002\u001a\u0007\u001a\u0002\u001b\u0007"+
		"\u001b\u0002\u001c\u0007\u001c\u0002\u001d\u0007\u001d\u0002\u001e\u0007"+
		"\u001e\u0002\u001f\u0007\u001f\u0002 \u0007 \u0002!\u0007!\u0002\"\u0007"+
		"\"\u0002#\u0007#\u0002$\u0007$\u0002%\u0007%\u0002&\u0007&\u0002\'\u0007"+
		"\'\u0002(\u0007(\u0002)\u0007)\u0002*\u0007*\u0002+\u0007+\u0002,\u0007"+
		",\u0002-\u0007-\u0002.\u0007.\u0002/\u0007/\u00020\u00070\u00021\u0007"+
		"1\u00022\u00072\u00023\u00073\u00024\u00074\u00025\u00075\u00026\u0007"+
		"6\u00027\u00077\u00028\u00078\u00029\u00079\u0002:\u0007:\u0002;\u0007"+
		";\u0002<\u0007<\u0002=\u0007=\u0002>\u0007>\u0002?\u0007?\u0002@\u0007"+
		"@\u0002A\u0007A\u0002B\u0007B\u0002C\u0007C\u0002D\u0007D\u0002E\u0007"+
		"E\u0002F\u0007F\u0002G\u0007G\u0002H\u0007H\u0002I\u0007I\u0002J\u0007"+
		"J\u0002K\u0007K\u0002L\u0007L\u0002M\u0007M\u0002N\u0007N\u0002O\u0007"+
		"O\u0002P\u0007P\u0002Q\u0007Q\u0002R\u0007R\u0002S\u0007S\u0002T\u0007"+
		"T\u0002U\u0007U\u0002V\u0007V\u0002W\u0007W\u0002X\u0007X\u0002Y\u0007"+
		"Y\u0002Z\u0007Z\u0002[\u0007[\u0002\\\u0007\\\u0002]\u0007]\u0002^\u0007"+
		"^\u0002_\u0007_\u0001\u0000\u0001\u0000\u0001\u0000\u0001\u0001\u0001"+
		"\u0001\u0001\u0001\u0001\u0002\u0001\u0002\u0001\u0002\u0001\u0003\u0001"+
		"\u0003\u0001\u0003\u0001\u0004\u0001\u0004\u0001\u0004\u0001\u0005\u0001"+
		"\u0005\u0001\u0005\u0001\u0005\u0001\u0005\u0001\u0005\u0001\u0005\u0001"+
		"\u0005\u0001\u0005\u0001\u0005\u0001\u0005\u0001\u0005\u0001\u0005\u0003"+
		"\u0005\u00dd\b\u0005\u0001\u0005\u0001\u0005\u0001\u0005\u0003\u0005\u00e2"+
		"\b\u0005\u0001\u0005\u0001\u0005\u0003\u0005\u00e6\b\u0005\u0001\u0005"+
		"\u0001\u0005\u0001\u0005\u0001\u0005\u0003\u0005\u00ec\b\u0005\u0001\u0005"+
		"\u0001\u0005\u0003\u0005\u00f0\b\u0005\u0001\u0005\u0001\u0005\u0001\u0005"+
		"\u0001\u0005\u0001\u0005\u0001\u0005\u0001\u0005\u0001\u0005\u0001\u0005"+
		"\u0001\u0005\u0001\u0005\u0001\u0005\u0001\u0005\u0001\u0005\u0001\u0005"+
		"\u0001\u0005\u0001\u0005\u0001\u0005\u0001\u0005\u0003\u0005\u0105\b\u0005"+
		"\u0001\u0005\u0001\u0005\u0003\u0005\u0109\b\u0005\u0001\u0005\u0001\u0005"+
		"\u0003\u0005\u010d\b\u0005\u0001\u0005\u0001\u0005\u0003\u0005\u0111\b"+
		"\u0005\u0001\u0005\u0001\u0005\u0001\u0005\u0001\u0005\u0001\u0005\u0001"+
		"\u0005\u0003\u0005\u0119\b\u0005\u0001\u0005\u0001\u0005\u0003\u0005\u011d"+
		"\b\u0005\u0001\u0005\u0003\u0005\u0120\b\u0005\u0001\u0005\u0001\u0005"+
		"\u0001\u0005\u0001\u0005\u0001\u0005\u0003\u0005\u0127\b\u0005\u0001\u0005"+
		"\u0001\u0005\u0001\u0005\u0001\u0005\u0001\u0005\u0005\u0005\u012e\b\u0005"+
		"\n\u0005\f\u0005\u0131\t\u0005\u0001\u0005\u0001\u0005\u0001\u0005\u0003"+
		"\u0005\u0136\b\u0005\u0001\u0005\u0001\u0005\u0003\u0005\u013a\b\u0005"+
		"\u0001\u0005\u0001\u0005\u0001\u0005\u0001\u0005\u0003\u0005\u0140\b\u0005"+
		"\u0001\u0005\u0001\u0005\u0001\u0005\u0001\u0005\u0001\u0005\u0003\u0005"+
		"\u0147\b\u0005\u0001\u0005\u0001\u0005\u0001\u0005\u0001\u0005\u0001\u0005"+
		"\u0001\u0005\u0001\u0005\u0003\u0005\u0150\b\u0005\u0001\u0005\u0001\u0005"+
		"\u0001\u0005\u0001\u0005\u0001\u0005\u0001\u0005\u0001\u0005\u0001\u0005"+
		"\u0001\u0005\u0001\u0005\u0003\u0005\u015c\b\u0005\u0001\u0005\u0001\u0005"+
		"\u0001\u0005\u0001\u0005\u0001\u0005\u0001\u0005\u0001\u0005\u0003\u0005"+
		"\u0165\b\u0005\u0001\u0005\u0001\u0005\u0001\u0005\u0001\u0005\u0003\u0005"+
		"\u016b\b\u0005\u0001\u0005\u0001\u0005\u0001\u0005\u0001\u0005\u0001\u0005"+
		"\u0001\u0005\u0001\u0005\u0001\u0005\u0001\u0005\u0003\u0005\u0176\b\u0005"+
		"\u0001\u0005\u0001\u0005\u0001\u0005\u0001\u0005\u0001\u0005\u0001\u0005"+
		"\u0003\u0005\u017e\b\u0005\u0001\u0005\u0001\u0005\u0001\u0005\u0001\u0005"+
		"\u0001\u0005\u0001\u0005\u0003\u0005\u0186\b\u0005\u0001\u0005\u0001\u0005"+
		"\u0001\u0005\u0001\u0005\u0001\u0005\u0003\u0005\u018d\b\u0005\u0001\u0005"+
		"\u0001\u0005\u0001\u0005\u0001\u0005\u0001\u0005\u0001\u0005\u0001\u0005"+
		"\u0001\u0005\u0003\u0005\u0197\b\u0005\u0001\u0005\u0001\u0005\u0001\u0005"+
		"\u0001\u0005\u0001\u0005\u0003\u0005\u019e\b\u0005\u0001\u0005\u0001\u0005"+
		"\u0001\u0005\u0001\u0005\u0001\u0005\u0001\u0005\u0001\u0005\u0001\u0005"+
		"\u0001\u0005\u0001\u0005\u0001\u0005\u0001\u0005\u0001\u0005\u0001\u0005"+
		"\u0001\u0005\u0001\u0005\u0001\u0005\u0001\u0005\u0001\u0005\u0001\u0005"+
		"\u0001\u0005\u0001\u0005\u0001\u0005\u0001\u0005\u0001\u0005\u0005\u0005"+
		"\u01b9\b\u0005\n\u0005\f\u0005\u01bc\t\u0005\u0003\u0005\u01be\b\u0005"+
		"\u0001\u0005\u0003\u0005\u01c1\b\u0005\u0001\u0005\u0001\u0005\u0003\u0005"+
		"\u01c5\b\u0005\u0001\u0005\u0001\u0005\u0001\u0005\u0001\u0005\u0003\u0005"+
		"\u01cb\b\u0005\u0001\u0005\u0001\u0005\u0001\u0005\u0003\u0005\u01d0\b"+
		"\u0005\u0001\u0005\u0001\u0005\u0001\u0005\u0001\u0005\u0001\u0005\u0003"+
		"\u0005\u01d7\b\u0005\u0001\u0005\u0001\u0005\u0001\u0005\u0003\u0005\u01dc"+
		"\b\u0005\u0001\u0005\u0001\u0005\u0003\u0005\u01e0\b\u0005\u0001\u0005"+
		"\u0001\u0005\u0001\u0005\u0001\u0005\u0001\u0005\u0001\u0005\u0003\u0005"+
		"\u01e8\b\u0005\u0001\u0005\u0001\u0005\u0001\u0005\u0001\u0005\u0003\u0005"+
		"\u01ee\b\u0005\u0001\u0005\u0001\u0005\u0003\u0005\u01f2\b\u0005\u0001"+
		"\u0005\u0001\u0005\u0001\u0005\u0001\u0005\u0001\u0005\u0001\u0005\u0001"+
		"\u0005\u0001\u0005\u0001\u0005\u0001\u0005\u0001\u0005\u0001\u0005\u0003"+
		"\u0005\u0200\b\u0005\u0001\u0005\u0001\u0005\u0001\u0005\u0001\u0005\u0001"+
		"\u0005\u0001\u0005\u0003\u0005\u0208\b\u0005\u0001\u0005\u0001\u0005\u0001"+
		"\u0005\u0001\u0005\u0001\u0005\u0001\u0005\u0001\u0005\u0001\u0005\u0001"+
		"\u0005\u0001\u0005\u0001\u0005\u0001\u0005\u0001\u0005\u0001\u0005\u0001"+
		"\u0005\u0001\u0005\u0001\u0005\u0003\u0005\u021b\b\u0005\u0001\u0005\u0001"+
		"\u0005\u0001\u0005\u0001\u0005\u0001\u0005\u0001\u0005\u0001\u0005\u0001"+
		"\u0005\u0001\u0005\u0001\u0005\u0001\u0005\u0001\u0005\u0001\u0005\u0001"+
		"\u0005\u0001\u0005\u0001\u0005\u0001\u0005\u0001\u0005\u0001\u0005\u0001"+
		"\u0005\u0001\u0005\u0005\u0005\u0232\b\u0005\n\u0005\f\u0005\u0235\t\u0005"+
		"\u0003\u0005\u0237\b\u0005\u0001\u0005\u0001\u0005\u0001\u0005\u0001\u0005"+
		"\u0001\u0005\u0001\u0005\u0001\u0005\u0001\u0005\u0003\u0005\u0241\b\u0005"+
		"\u0001\u0005\u0001\u0005\u0003\u0005\u0245\b\u0005\u0001\u0005\u0001\u0005"+
		"\u0001\u0005\u0001\u0005\u0001\u0005\u0003\u0005\u024c\b\u0005\u0001\u0005"+
		"\u0001\u0005\u0001\u0005\u0001\u0005\u0001\u0005\u0001\u0005\u0005\u0005"+
		"\u0254\b\u0005\n\u0005\f\u0005\u0257\t\u0005\u0001\u0005\u0001\u0005\u0001"+
		"\u0005\u0003\u0005\u025c\b\u0005\u0001\u0005\u0001\u0005\u0001\u0005\u0003"+
		"\u0005\u0261\b\u0005\u0001\u0005\u0001\u0005\u0003\u0005\u0265\b\u0005"+
		"\u0001\u0005\u0001\u0005\u0001\u0005\u0001\u0005\u0003\u0005\u026b\b\u0005"+
		"\u0001\u0005\u0001\u0005\u0001\u0005\u0001\u0005\u0001\u0005\u0005\u0005"+
		"\u0272\b\u0005\n\u0005\f\u0005\u0275\t\u0005\u0001\u0005\u0001\u0005\u0001"+
		"\u0005\u0003\u0005\u027a\b\u0005\u0001\u0005\u0001\u0005\u0003\u0005\u027e"+
		"\b\u0005\u0001\u0005\u0001\u0005\u0001\u0005\u0001\u0005\u0001\u0005\u0003"+
		"\u0005\u0285\b\u0005\u0001\u0005\u0001\u0005\u0003\u0005\u0289\b\u0005"+
		"\u0001\u0005\u0001\u0005\u0001\u0005\u0001\u0005\u0005\u0005\u028f\b\u0005"+
		"\n\u0005\f\u0005\u0292\t\u0005\u0001\u0005\u0001\u0005\u0003\u0005\u0296"+
		"\b\u0005\u0001\u0005\u0001\u0005\u0003\u0005\u029a\b\u0005\u0001\u0005"+
		"\u0001\u0005\u0001\u0005\u0001\u0005\u0001\u0005\u0001\u0005\u0003\u0005"+
		"\u02a2\b\u0005\u0001\u0005\u0001\u0005\u0001\u0005\u0001\u0005\u0005\u0005"+
		"\u02a8\b\u0005\n\u0005\f\u0005\u02ab\t\u0005\u0001\u0005\u0001\u0005\u0003"+
		"\u0005\u02af\b\u0005\u0001\u0005\u0001\u0005\u0003\u0005\u02b3\b\u0005"+
		"\u0001\u0005\u0001\u0005\u0001\u0005\u0001\u0005\u0001\u0005\u0001\u0005"+
		"\u0001\u0005\u0001\u0005\u0003\u0005\u02bd\b\u0005\u0001\u0005\u0001\u0005"+
		"\u0001\u0005\u0005\u0005\u02c2\b\u0005\n\u0005\f\u0005\u02c5\t\u0005\u0001"+
		"\u0005\u0001\u0005\u0003\u0005\u02c9\b\u0005\u0001\u0005\u0001\u0005\u0003"+
		"\u0005\u02cd\b\u0005\u0001\u0005\u0001\u0005\u0001\u0005\u0001\u0005\u0001"+
		"\u0005\u0001\u0005\u0001\u0005\u0001\u0005\u0003\u0005\u02d7\b\u0005\u0001"+
		"\u0005\u0003\u0005\u02da\b\u0005\u0001\u0005\u0001\u0005\u0001\u0005\u0001"+
		"\u0005\u0001\u0005\u0005\u0005\u02e1\b\u0005\n\u0005\f\u0005\u02e4\t\u0005"+
		"\u0001\u0005\u0001\u0005\u0003\u0005\u02e8\b\u0005\u0001\u0005\u0001\u0005"+
		"\u0001\u0005\u0001\u0005\u0003\u0005\u02ee\b\u0005\u0001\u0005\u0001\u0005"+
		"\u0001\u0005\u0001\u0005\u0001\u0005\u0001\u0005\u0001\u0005\u0001\u0005"+
		"\u0001\u0005\u0001\u0005\u0001\u0005\u0001\u0005\u0001\u0005\u0001\u0005"+
		"\u0001\u0005\u0001\u0005\u0001\u0005\u0001\u0005\u0001\u0005\u0001\u0005"+
		"\u0001\u0005\u0001\u0005\u0003\u0005\u0306\b\u0005\u0001\u0005\u0001\u0005"+
		"\u0001\u0005\u0001\u0005\u0003\u0005\u030c\b\u0005\u0003\u0005\u030e\b"+
		"\u0005\u0001\u0005\u0001\u0005\u0001\u0005\u0001\u0005\u0003\u0005\u0314"+
		"\b\u0005\u0001\u0005\u0001\u0005\u0001\u0005\u0001\u0005\u0003\u0005\u031a"+
		"\b\u0005\u0003\u0005\u031c\b\u0005\u0001\u0005\u0001\u0005\u0001\u0005"+
		"\u0001\u0005\u0001\u0005\u0001\u0005\u0003\u0005\u0324\b\u0005\u0003\u0005"+
		"\u0326\b\u0005\u0001\u0005\u0001\u0005\u0001\u0005\u0001\u0005\u0003\u0005"+
		"\u032c\b\u0005\u0001\u0005\u0001\u0005\u0001\u0005\u0001\u0005\u0003\u0005"+
		"\u0332\b\u0005\u0003\u0005\u0334\b\u0005\u0001\u0005\u0001\u0005\u0001"+
		"\u0005\u0001\u0005\u0001\u0005\u0001\u0005\u0001\u0005\u0001\u0005\u0001"+
		"\u0005\u0001\u0005\u0001\u0005\u0001\u0005\u0001\u0005\u0003\u0005\u0343"+
		"\b\u0005\u0001\u0005\u0001\u0005\u0001\u0005\u0003\u0005\u0348\b\u0005"+
		"\u0001\u0005\u0001\u0005\u0001\u0005\u0001\u0005\u0001\u0005\u0003\u0005"+
		"\u034f\b\u0005\u0001\u0005\u0001\u0005\u0001\u0005\u0001\u0005\u0001\u0005"+
		"\u0001\u0005\u0001\u0005\u0001\u0005\u0001\u0005\u0001\u0005\u0003\u0005"+
		"\u035b\b\u0005\u0003\u0005\u035d\b\u0005\u0001\u0005\u0001\u0005\u0001"+
		"\u0005\u0001\u0005\u0001\u0005\u0001\u0005\u0003\u0005\u0365\b\u0005\u0003"+
		"\u0005\u0367\b\u0005\u0001\u0005\u0001\u0005\u0001\u0005\u0001\u0005\u0001"+
		"\u0005\u0001\u0005\u0001\u0005\u0001\u0005\u0001\u0005\u0001\u0005\u0001"+
		"\u0005\u0001\u0005\u0001\u0005\u0001\u0005\u0005\u0005\u0377\b\u0005\n"+
		"\u0005\f\u0005\u037a\t\u0005\u0003\u0005\u037c\b\u0005\u0001\u0005\u0001"+
		"\u0005\u0003\u0005\u0380\b\u0005\u0001\u0005\u0001\u0005\u0003\u0005\u0384"+
		"\b\u0005\u0001\u0005\u0001\u0005\u0001\u0005\u0001\u0005\u0001\u0005\u0001"+
		"\u0005\u0001\u0005\u0001\u0005\u0001\u0005\u0001\u0005\u0001\u0005\u0001"+
		"\u0005\u0001\u0005\u0001\u0005\u0005\u0005\u0394\b\u0005\n\u0005\f\u0005"+
		"\u0397\t\u0005\u0003\u0005\u0399\b\u0005\u0001\u0005\u0001\u0005\u0001"+
		"\u0005\u0001\u0005\u0001\u0005\u0001\u0005\u0001\u0005\u0001\u0005\u0001"+
		"\u0005\u0001\u0005\u0001\u0005\u0001\u0005\u0001\u0005\u0001\u0005\u0003"+
		"\u0005\u03a9\b\u0005\u0001\u0005\u0001\u0005\u0001\u0005\u0001\u0005\u0001"+
		"\u0005\u0001\u0005\u0005\u0005\u03b1\b\u0005\n\u0005\f\u0005\u03b4\t\u0005"+
		"\u0001\u0005\u0001\u0005\u0003\u0005\u03b8\b\u0005\u0001\u0005\u0001\u0005"+
		"\u0001\u0005\u0001\u0005\u0003\u0005\u03be\b\u0005\u0001\u0005\u0003\u0005"+
		"\u03c1\b\u0005\u0001\u0005\u0001\u0005\u0001\u0005\u0001\u0005\u0001\u0005"+
		"\u0004\u0005\u03c8\b\u0005\u000b\u0005\f\u0005\u03c9\u0001\u0005\u0001"+
		"\u0005\u0001\u0005\u0003\u0005\u03cf\b\u0005\u0001\u0005\u0003\u0005\u03d2"+
		"\b\u0005\u0001\u0005\u0003\u0005\u03d5\b\u0005\u0001\u0005\u0003\u0005"+
		"\u03d8\b\u0005\u0001\u0005\u0001\u0005\u0001\u0005\u0003\u0005\u03dd\b"+
		"\u0005\u0001\u0005\u0001\u0005\u0001\u0005\u0001\u0005\u0001\u0005\u0001"+
		"\u0005\u0001\u0005\u0001\u0005\u0001\u0005\u0003\u0005\u03e8\b\u0005\u0001"+
		"\u0006\u0003\u0006\u03eb\b\u0006\u0001\u0006\u0001\u0006\u0001\u0007\u0001"+
		"\u0007\u0003\u0007\u03f1\b\u0007\u0001\u0007\u0001\u0007\u0001\u0007\u0005"+
		"\u0007\u03f6\b\u0007\n\u0007\f\u0007\u03f9\t\u0007\u0001\b\u0001\b\u0003"+
		"\b\u03fd\b\b\u0001\t\u0001\t\u0001\t\u0001\t\u0003\t\u0403\b\t\u0001\t"+
		"\u0001\t\u0003\t\u0407\b\t\u0001\t\u0001\t\u0003\t\u040b\b\t\u0001\n\u0001"+
		"\n\u0001\n\u0001\n\u0003\n\u0411\b\n\u0001\u000b\u0001\u000b\u0001\u000b"+
		"\u0001\u000b\u0001\f\u0001\f\u0001\f\u0005\f\u041a\b\f\n\f\f\f\u041d\t"+
		"\f\u0001\r\u0001\r\u0001\r\u0001\r\u0001\u000e\u0001\u000e\u0003\u000e"+
		"\u0425\b\u000e\u0001\u000f\u0001\u000f\u0001\u000f\u0001\u000f\u0001\u000f"+
		"\u0001\u000f\u0005\u000f\u042d\b\u000f\n\u000f\f\u000f\u0430\t\u000f\u0003"+
		"\u000f\u0432\b\u000f\u0001\u000f\u0001\u000f\u0001\u000f\u0003\u000f\u0437"+
		"\b\u000f\u0003\u000f\u0439\b\u000f\u0001\u000f\u0001\u000f\u0001\u000f"+
		"\u0003\u000f\u043e\b\u000f\u0001\u000f\u0001\u000f\u0001\u000f\u0003\u000f"+
		"\u0443\b\u000f\u0001\u000f\u0001\u000f\u0001\u000f\u0001\u000f\u0003\u000f"+
		"\u0449\b\u000f\u0003\u000f\u044b\b\u000f\u0001\u000f\u0001\u000f\u0001"+
		"\u000f\u0003\u000f\u0450\b\u000f\u0003\u000f\u0452\b\u000f\u0001\u000f"+
		"\u0001\u000f\u0001\u000f\u0003\u000f\u0457\b\u000f\u0003\u000f\u0459\b"+
		"\u000f\u0003\u000f\u045b\b\u000f\u0001\u0010\u0001\u0010\u0001\u0010\u0003"+
		"\u0010\u0460\b\u0010\u0001\u0010\u0001\u0010\u0001\u0011\u0001\u0011\u0001"+
		"\u0011\u0003\u0011\u0467\b\u0011\u0001\u0012\u0001\u0012\u0001\u0013\u0001"+
		"\u0013\u0001\u0013\u0001\u0013\u0001\u0013\u0001\u0013\u0003\u0013\u0471"+
		"\b\u0013\u0001\u0013\u0001\u0013\u0001\u0013\u0001\u0013\u0003\u0013\u0477"+
		"\b\u0013\u0001\u0013\u0005\u0013\u047a\b\u0013\n\u0013\f\u0013\u047d\t"+
		"\u0013\u0001\u0014\u0001\u0014\u0001\u0014\u0001\u0014\u0001\u0014\u0001"+
		"\u0014\u0001\u0014\u0005\u0014\u0486\b\u0014\n\u0014\f\u0014\u0489\t\u0014"+
		"\u0001\u0014\u0001\u0014\u0001\u0014\u0001\u0014\u0003\u0014\u048f\b\u0014"+
		"\u0001\u0015\u0001\u0015\u0003\u0015\u0493\b\u0015\u0001\u0015\u0001\u0015"+
		"\u0003\u0015\u0497\b\u0015\u0001\u0016\u0001\u0016\u0003\u0016\u049b\b"+
		"\u0016\u0001\u0016\u0001\u0016\u0001\u0016\u0005\u0016\u04a0\b\u0016\n"+
		"\u0016\f\u0016\u04a3\t\u0016\u0001\u0016\u0001\u0016\u0001\u0016\u0001"+
		"\u0016\u0005\u0016\u04a9\b\u0016\n\u0016\f\u0016\u04ac\t\u0016\u0003\u0016"+
		"\u04ae\b\u0016\u0001\u0016\u0001\u0016\u0003\u0016\u04b2\b\u0016\u0001"+
		"\u0016\u0001\u0016\u0001\u0016\u0003\u0016\u04b7\b\u0016\u0001\u0016\u0001"+
		"\u0016\u0003\u0016\u04bb\b\u0016\u0001\u0016\u0001\u0016\u0001\u0016\u0001"+
		"\u0016\u0005\u0016\u04c1\b\u0016\n\u0016\f\u0016\u04c4\t\u0016\u0003\u0016"+
		"\u04c6\b\u0016\u0001\u0017\u0003\u0017\u04c9\b\u0017\u0001\u0017\u0001"+
		"\u0017\u0001\u0017\u0005\u0017\u04ce\b\u0017\n\u0017\f\u0017\u04d1\t\u0017"+
		"\u0001\u0018\u0001\u0018\u0001\u0018\u0001\u0018\u0001\u0018\u0001\u0018"+
		"\u0005\u0018\u04d9\b\u0018\n\u0018\f\u0018\u04dc\t\u0018\u0003\u0018\u04de"+
		"\b\u0018\u0001\u0018\u0001\u0018\u0001\u0018\u0001\u0018\u0001\u0018\u0001"+
		"\u0018\u0005\u0018\u04e6\b\u0018\n\u0018\f\u0018\u04e9\t\u0018\u0003\u0018"+
		"\u04eb\b\u0018\u0001\u0018\u0001\u0018\u0001\u0018\u0001\u0018\u0001\u0018"+
		"\u0001\u0018\u0001\u0018\u0005\u0018\u04f4\b\u0018\n\u0018\f\u0018\u04f7"+
		"\t\u0018\u0001\u0018\u0001\u0018\u0003\u0018\u04fb\b\u0018\u0001\u0019"+
		"\u0001\u0019\u0001\u0019\u0001\u0019\u0005\u0019\u0501\b\u0019\n\u0019"+
		"\f\u0019\u0504\t\u0019\u0003\u0019\u0506\b\u0019\u0001\u0019\u0001\u0019"+
		"\u0003\u0019\u050a\b\u0019\u0001\u001a\u0001\u001a\u0001\u001a\u0001\u001a"+
		"\u0001\u001a\u0001\u001a\u0001\u001b\u0003\u001b\u0513\b\u001b\u0001\u001b"+
		"\u0001\u001b\u0001\u001b\u0001\u001b\u0001\u001b\u0005\u001b\u051a\b\u001b"+
		"\n\u001b\f\u001b\u051d\t\u001b\u0003\u001b\u051f\b\u001b\u0001\u001b\u0001"+
		"\u001b\u0001\u001b\u0001\u001b\u0001\u001b\u0005\u001b\u0526\b\u001b\n"+
		"\u001b\f\u001b\u0529\t\u001b\u0003\u001b\u052b\b\u001b\u0001\u001b\u0003"+
		"\u001b\u052e\b\u001b\u0001\u001c\u0001\u001c\u0003\u001c\u0532\b\u001c"+
		"\u0001\u001c\u0001\u001c\u0001\u001c\u0001\u001c\u0001\u001c\u0001\u001d"+
		"\u0001\u001d\u0001\u001e\u0001\u001e\u0003\u001e\u053d\b\u001e\u0001\u001e"+
		"\u0003\u001e\u0540\b\u001e\u0001\u001e\u0001\u001e\u0001\u001e\u0001\u001e"+
		"\u0001\u001e\u0003\u001e\u0547\b\u001e\u0001\u001e\u0003\u001e\u054a\b"+
		"\u001e\u0001\u001f\u0001\u001f\u0001\u001f\u0001\u001f\u0001\u001f\u0001"+
		"\u001f\u0001\u001f\u0001\u001f\u0001\u001f\u0001\u001f\u0001\u001f\u0001"+
		"\u001f\u0001\u001f\u0001\u001f\u0001\u001f\u0001\u001f\u0001\u001f\u0003"+
		"\u001f\u055d\b\u001f\u0005\u001f\u055f\b\u001f\n\u001f\f\u001f\u0562\t"+
		"\u001f\u0001 \u0003 \u0565\b \u0001 \u0001 \u0003 \u0569\b \u0001 \u0001"+
		" \u0003 \u056d\b \u0001 \u0001 \u0003 \u0571\b \u0003 \u0573\b \u0001"+
		"!\u0001!\u0001!\u0001!\u0001!\u0001!\u0001!\u0005!\u057c\b!\n!\f!\u057f"+
		"\t!\u0001!\u0001!\u0003!\u0583\b!\u0001\"\u0001\"\u0001\"\u0001\"\u0001"+
		"\"\u0001\"\u0001\"\u0003\"\u058c\b\"\u0001#\u0001#\u0001$\u0001$\u0001"+
		"$\u0003$\u0593\b$\u0001$\u0003$\u0596\b$\u0001%\u0001%\u0001%\u0001%\u0003"+
		"%\u059c\b%\u0001&\u0001&\u0001&\u0001&\u0001&\u0001&\u0001&\u0001&\u0005"+
		"&\u05a6\b&\n&\f&\u05a9\t&\u0003&\u05ab\b&\u0001&\u0001&\u0001&\u0001&"+
		"\u0001&\u0005&\u05b2\b&\n&\f&\u05b5\t&\u0003&\u05b7\b&\u0001&\u0001&\u0001"+
		"&\u0001&\u0005&\u05bd\b&\n&\f&\u05c0\t&\u0003&\u05c2\b&\u0001&\u0003&"+
		"\u05c5\b&\u0001&\u0001&\u0001&\u0003&\u05ca\b&\u0001&\u0003&\u05cd\b&"+
		"\u0001&\u0001&\u0001&\u0001&\u0001&\u0001&\u0001&\u0001&\u0005&\u05d7"+
		"\b&\n&\f&\u05da\t&\u0003&\u05dc\b&\u0001&\u0001&\u0001&\u0001&\u0005&"+
		"\u05e2\b&\n&\f&\u05e5\t&\u0001&\u0001&\u0003&\u05e9\b&\u0001&\u0001&\u0003"+
		"&\u05ed\b&\u0003&\u05ef\b&\u0003&\u05f1\b&\u0001\'\u0001\'\u0001\'\u0001"+
		"\'\u0001(\u0001(\u0001(\u0001(\u0001(\u0001(\u0001(\u0001(\u0001(\u0003"+
		"(\u0600\b(\u0003(\u0602\b(\u0001)\u0001)\u0001)\u0001)\u0001)\u0001)\u0001"+
		")\u0001)\u0001)\u0003)\u060d\b)\u0001*\u0001*\u0001*\u0001*\u0001*\u0001"+
		"*\u0001*\u0001*\u0001*\u0001*\u0001*\u0001*\u0001*\u0001*\u0001*\u0001"+
		"*\u0001*\u0001*\u0001*\u0003*\u0622\b*\u0001+\u0001+\u0001+\u0001+\u0001"+
		"+\u0001+\u0005+\u062a\b+\n+\f+\u062d\t+\u0001+\u0001+\u0001,\u0001,\u0001"+
		",\u0001,\u0001-\u0001-\u0003-\u0637\b-\u0001-\u0001-\u0003-\u063b\b-\u0003"+
		"-\u063d\b-\u0001.\u0001.\u0001.\u0001.\u0005.\u0643\b.\n.\f.\u0646\t."+
		"\u0001.\u0001.\u0001/\u0001/\u0003/\u064c\b/\u0001/\u0001/\u0001/\u0001"+
		"/\u0001/\u0001/\u0001/\u0001/\u0001/\u0005/\u0657\b/\n/\f/\u065a\t/\u0001"+
		"/\u0001/\u0001/\u0003/\u065f\b/\u0001/\u0001/\u0003/\u0663\b/\u0001/\u0001"+
		"/\u0001/\u0001/\u0001/\u0005/\u066a\b/\n/\f/\u066d\t/\u0001/\u0001/\u0001"+
		"/\u0003/\u0672\b/\u0001/\u0001/\u0001/\u0001/\u0001/\u0001/\u0001/\u0001"+
		"/\u0001/\u0001/\u0001/\u0003/\u067f\b/\u00010\u00010\u00011\u00011\u0001"+
		"1\u00031\u0686\b1\u00011\u00011\u00031\u068a\b1\u00011\u00011\u00011\u0001"+
		"1\u00011\u00011\u00051\u0692\b1\n1\f1\u0695\t1\u00012\u00012\u00012\u0001"+
		"2\u00012\u00012\u00012\u00032\u069e\b2\u00012\u00012\u00032\u06a2\b2\u0001"+
		"2\u00032\u06a5\b2\u00012\u00012\u00012\u00012\u00012\u00032\u06ac\b2\u0001"+
		"2\u00012\u00012\u00012\u00012\u00012\u00012\u00012\u00012\u00012\u0001"+
		"2\u00012\u00012\u00012\u00032\u06bc\b2\u00012\u00012\u00012\u00012\u0001"+
		"2\u00012\u00032\u06c4\b2\u00012\u00012\u00012\u00012\u00012\u00052\u06cb"+
		"\b2\n2\f2\u06ce\t2\u00012\u00012\u00012\u00032\u06d3\b2\u00012\u00012"+
		"\u00012\u00012\u00012\u00012\u00032\u06db\b2\u00012\u00012\u00012\u0001"+
		"2\u00032\u06e1\b2\u00012\u00012\u00032\u06e5\b2\u00012\u00012\u00012\u0003"+
		"2\u06ea\b2\u00012\u00012\u00012\u00032\u06ef\b2\u00013\u00013\u00013\u0001"+
		"3\u00013\u00053\u06f6\b3\n3\f3\u06f9\t3\u00013\u00013\u00014\u00014\u0001"+
		"4\u00034\u0700\b4\u00014\u00014\u00014\u00034\u0705\b4\u00014\u00014\u0001"+
		"4\u00014\u00014\u00014\u00014\u00014\u00014\u00014\u00014\u00034\u0712"+
		"\b4\u00014\u00014\u00014\u00014\u00014\u00014\u00014\u00014\u00014\u0005"+
		"4\u071d\b4\n4\f4\u0720\t4\u00015\u00015\u00015\u00015\u00015\u00015\u0001"+
		"5\u00015\u00015\u00015\u00015\u00015\u00015\u00035\u072f\b5\u00015\u0001"+
		"5\u00015\u00015\u00015\u00015\u00015\u00015\u00015\u00015\u00015\u0001"+
		"5\u00015\u00015\u00015\u00015\u00015\u00015\u00045\u0743\b5\u000b5\f5"+
		"\u0744\u00015\u00015\u00015\u00015\u00015\u00015\u00015\u00055\u074e\b"+
		"5\n5\f5\u0751\t5\u00015\u00015\u00015\u00015\u00015\u00035\u0758\b5\u0001"+
		"5\u00015\u00015\u00035\u075d\b5\u00015\u00015\u00015\u00035\u0762\b5\u0001"+
		"5\u00015\u00015\u00015\u00015\u00015\u00015\u00015\u00015\u00055\u076d"+
		"\b5\n5\f5\u0770\t5\u00015\u00015\u00015\u00035\u0775\b5\u00015\u00015"+
		"\u00015\u00015\u00015\u00035\u077c\b5\u00015\u00015\u00015\u00035\u0781"+
		"\b5\u00015\u00035\u0784\b5\u00015\u00035\u0787\b5\u00015\u00015\u0001"+
		"5\u00035\u078c\b5\u00015\u00015\u00015\u00055\u0791\b5\n5\f5\u0794\t5"+
		"\u00035\u0796\b5\u00015\u00015\u00015\u00015\u00015\u00055\u079d\b5\n"+
		"5\f5\u07a0\t5\u00035\u07a2\b5\u00015\u00015\u00035\u07a6\b5\u00015\u0003"+
		"5\u07a9\b5\u00015\u00035\u07ac\b5\u00015\u00015\u00015\u00015\u00015\u0001"+
		"5\u00015\u00015\u00015\u00015\u00015\u00055\u07b9\b5\n5\f5\u07bc\t5\u0003"+
		"5\u07be\b5\u00015\u00015\u00015\u00015\u00015\u00015\u00015\u00015\u0001"+
		"5\u00015\u00015\u00015\u00015\u00015\u00015\u00045\u07cf\b5\u000b5\f5"+
		"\u07d0\u00015\u00015\u00035\u07d5\b5\u00015\u00015\u00015\u00015\u0004"+
		"5\u07db\b5\u000b5\f5\u07dc\u00015\u00015\u00035\u07e1\b5\u00015\u0001"+
		"5\u00015\u00015\u00015\u00015\u00015\u00015\u00015\u00015\u00015\u0001"+
		"5\u00015\u00015\u00015\u00015\u00015\u00015\u00015\u00015\u00015\u0001"+
		"5\u00035\u07f9\b5\u00015\u00015\u00015\u00015\u00015\u00015\u00015\u0001"+
		"5\u00055\u0803\b5\n5\f5\u0806\t5\u00035\u0808\b5\u00015\u00015\u00015"+
		"\u00015\u00015\u00055\u080f\b5\n5\f5\u0812\t5\u00035\u0814\b5\u00015\u0001"+
		"5\u00015\u00015\u00015\u00015\u00015\u00035\u081d\b5\u00015\u00015\u0001"+
		"5\u00015\u00035\u0823\b5\u00015\u00015\u00015\u00015\u00035\u0829\b5\u0001"+
		"5\u00015\u00015\u00015\u00035\u082f\b5\u00015\u00015\u00015\u00015\u0001"+
		"5\u00035\u0836\b5\u00015\u00015\u00015\u00035\u083b\b5\u00015\u00015\u0001"+
		"5\u00015\u00015\u00015\u00015\u00015\u00035\u0845\b5\u00015\u00015\u0001"+
		"5\u00015\u00015\u00015\u00015\u00035\u084e\b5\u00015\u00015\u00015\u0001"+
		"5\u00015\u00015\u00015\u00015\u00015\u00015\u00015\u00015\u00015\u0001"+
		"5\u00015\u00015\u00015\u00015\u00055\u0862\b5\n5\f5\u0865\t5\u00035\u0867"+
		"\b5\u00015\u00035\u086a\b5\u00015\u00015\u00015\u00015\u00035\u0870\b"+
		"5\u00015\u00015\u00015\u00015\u00015\u00015\u00015\u00015\u00015\u0005"+
		"5\u087b\b5\n5\f5\u087e\t5\u00016\u00016\u00017\u00017\u00017\u00017\u0003"+
		"7\u0886\b7\u00018\u00018\u00018\u00018\u00038\u088c\b8\u00018\u00038\u088f"+
		"\b8\u00019\u00019\u00019\u00019\u00019\u00019\u00039\u0897\b9\u0001:\u0001"+
		":\u0001;\u0001;\u0001<\u0001<\u0001=\u0001=\u0003=\u08a1\b=\u0001=\u0001"+
		"=\u0001=\u0001=\u0003=\u08a7\b=\u0001>\u0001>\u0001?\u0001?\u0001@\u0001"+
		"@\u0001@\u0001@\u0001@\u0001@\u0005@\u08b3\b@\n@\f@\u08b6\t@\u0001@\u0001"+
		"@\u0001@\u0001@\u0001@\u0001@\u0003@\u08be\b@\u0001@\u0001@\u0001@\u0001"+
		"@\u0001@\u0003@\u08c5\b@\u0001@\u0001@\u0001@\u0003@\u08ca\b@\u0001@\u0001"+
		"@\u0001@\u0001@\u0001@\u0003@\u08d1\b@\u0001@\u0001@\u0001@\u0001@\u0001"+
		"@\u0001@\u0001@\u0001@\u0003@\u08db\b@\u0001@\u0001@\u0001@\u0003@\u08e0"+
		"\b@\u0001@\u0001@\u0001@\u0001@\u0001@\u0003@\u08e7\b@\u0001@\u0001@\u0001"+
		"@\u0001@\u0001@\u0001@\u0001@\u0001@\u0001@\u0001@\u0001@\u0001@\u0001"+
		"@\u0001@\u0001@\u0001@\u0001@\u0001@\u0001@\u0001@\u0001@\u0001@\u0005"+
		"@\u08ff\b@\n@\f@\u0902\t@\u0001@\u0001@\u0003@\u0906\b@\u0003@\u0908\b"+
		"@\u0001@\u0001@\u0001@\u0001@\u0001@\u0003@\u090f\b@\u0005@\u0911\b@\n"+
		"@\f@\u0914\t@\u0001A\u0001A\u0001A\u0001A\u0003A\u091a\bA\u0001B\u0001"+
		"B\u0003B\u091e\bB\u0001C\u0001C\u0001C\u0001C\u0001C\u0001D\u0001D\u0001"+
		"D\u0001D\u0001D\u0001D\u0001E\u0001E\u0001E\u0001E\u0003E\u092f\bE\u0001"+
		"E\u0001E\u0001E\u0001E\u0001E\u0001E\u0001E\u0001E\u0001E\u0001E\u0001"+
		"E\u0005E\u093c\bE\nE\fE\u093f\tE\u0001E\u0001E\u0001E\u0001E\u0003E\u0945"+
		"\bE\u0001E\u0001E\u0001E\u0001E\u0001E\u0001E\u0001E\u0003E\u094e\bE\u0001"+
		"E\u0001E\u0001E\u0001E\u0001E\u0001E\u0005E\u0956\bE\nE\fE\u0959\tE\u0001"+
		"E\u0001E\u0003E\u095d\bE\u0001E\u0001E\u0001E\u0001E\u0001E\u0005E\u0964"+
		"\bE\nE\fE\u0967\tE\u0001E\u0001E\u0003E\u096b\bE\u0001F\u0001F\u0001F"+
		"\u0001F\u0001F\u0001F\u0003F\u0973\bF\u0001G\u0001G\u0001G\u0001G\u0005"+
		"G\u0979\bG\nG\fG\u097c\tG\u0003G\u097e\bG\u0001G\u0001G\u0001G\u0001G"+
		"\u0003G\u0984\bG\u0001G\u0003G\u0987\bG\u0001G\u0001G\u0001G\u0001G\u0001"+
		"G\u0003G\u098e\bG\u0001G\u0001G\u0001G\u0001G\u0005G\u0994\bG\nG\fG\u0997"+
		"\tG\u0003G\u0999\bG\u0001G\u0001G\u0001G\u0001G\u0005G\u099f\bG\nG\fG"+
		"\u09a2\tG\u0003G\u09a4\bG\u0001H\u0001H\u0001H\u0001H\u0001H\u0001H\u0001"+
		"H\u0001H\u0001H\u0001H\u0001H\u0001H\u0001H\u0001H\u0001H\u0001H\u0001"+
		"H\u0001H\u0001H\u0001H\u0001H\u0001H\u0001H\u0001H\u0003H\u09be\bH\u0001"+
		"I\u0001I\u0001I\u0001I\u0001I\u0001I\u0001I\u0001I\u0001I\u0003I\u09c9"+
		"\bI\u0001J\u0001J\u0001J\u0003J\u09ce\bJ\u0001J\u0001J\u0001J\u0001J\u0001"+
		"J\u0005J\u09d5\bJ\nJ\fJ\u09d8\tJ\u0001K\u0001K\u0001K\u0001K\u0001K\u0001"+
		"K\u0001K\u0001K\u0005K\u09e2\bK\nK\fK\u09e5\tK\u0001K\u0001K\u0001K\u0001"+
		"K\u0001K\u0001K\u0001K\u0001K\u0001K\u0001K\u0001K\u0001K\u0003K\u09f3"+
		"\bK\u0001L\u0001L\u0003L\u09f7\bL\u0001L\u0001L\u0003L\u09fb\bL\u0001"+
		"L\u0001L\u0003L\u09ff\bL\u0001L\u0001L\u0001L\u0001L\u0003L\u0a05\bL\u0001"+
		"L\u0001L\u0003L\u0a09\bL\u0001L\u0001L\u0003L\u0a0d\bL\u0001L\u0001L\u0003"+
		"L\u0a11\bL\u0003L\u0a13\bL\u0001M\u0001M\u0001M\u0001M\u0001N\u0001N\u0001"+
		"N\u0001N\u0003N\u0a1d\bN\u0001O\u0001O\u0001O\u0001O\u0001O\u0003O\u0a24"+
		"\bO\u0001P\u0001P\u0001P\u0001P\u0001P\u0001P\u0001P\u0003P\u0a2d\bP\u0001"+
		"Q\u0001Q\u0001Q\u0001Q\u0001Q\u0003Q\u0a34\bQ\u0001R\u0001R\u0001R\u0001"+
		"R\u0001R\u0003R\u0a3b\bR\u0001S\u0001S\u0001S\u0005S\u0a40\bS\nS\fS\u0a43"+
		"\tS\u0001T\u0001T\u0001U\u0001U\u0001U\u0005U\u0a4a\bU\nU\fU\u0a4d\tU"+
		"\u0001V\u0001V\u0001V\u0001V\u0001V\u0001V\u0001W\u0001W\u0001X\u0001"+
		"X\u0001X\u0003X\u0a5a\bX\u0001Y\u0001Y\u0001Y\u0001Y\u0001Y\u0003Y\u0a61"+
		"\bY\u0001Z\u0001Z\u0001Z\u0005Z\u0a66\bZ\nZ\fZ\u0a69\tZ\u0001[\u0001["+
		"\u0001[\u0001[\u0001[\u0003[\u0a70\b[\u0001\\\u0003\\\u0a73\b\\\u0001"+
		"\\\u0001\\\u0003\\\u0a77\b\\\u0001\\\u0001\\\u0003\\\u0a7b\b\\\u0001\\"+
		"\u0003\\\u0a7e\b\\\u0001]\u0001]\u0001]\u0001]\u0003]\u0a84\b]\u0001]"+
		"\u0001]\u0001]\u0001^\u0001^\u0001^\u0003^\u0a8c\b^\u0001^\u0001^\u0001"+
		"_\u0001_\u0001_\u0000\u0007&>bhj\u0080\u0094`\u0000\u0002\u0004\u0006"+
		"\b\n\f\u000e\u0010\u0012\u0014\u0016\u0018\u001a\u001c\u001e \"$&(*,."+
		"02468:<>@BDFHJLNPRTVXZ\\^`bdfhjlnprtvxz|~\u0080\u0082\u0084\u0086\u0088"+
		"\u008a\u008c\u008e\u0090\u0092\u0094\u0096\u0098\u009a\u009c\u009e\u00a0"+
		"\u00a2\u00a4\u00a6\u00a8\u00aa\u00ac\u00ae\u00b0\u00b2\u00b4\u00b6\u00b8"+
		"\u00ba\u00bc\u00be\u0000\"\u0002\u0000\'\'\u00c9\u00c9\u0002\u0000FF|"+
		"|\u0002\u0000\u00d3\u00d3\u00e5\u00e5\u0002\u0000ddss\u0001\u0000\u0006"+
		"\u0007\u0002\u0000\u0105\u0105\u0107\u0107\u0002\u0000WWtt\u0001\u0000"+
		"\u00d0\u00d1\u0002\u0000``\u0098\u0098\u0002\u0000\u0118\u0118\u011d\u011d"+
		"\u0002\u0000VV\u00f6\u00f6\u0002\u0000  II\u0002\u0000``\u0082\u0082\u0002"+
		"\u0000\u0019\u0019LL\u0002\u0000##\u00e4\u00e4\u0002\u0000uu\u00d7\u00d7"+
		"\u0001\u0000\u0112\u0113\u0001\u0000\u0114\u0116\u0001\u0000\u0112\u0116"+
		"\u0002\u0000__\u00d2\u00d2\u0001\u0000\u010c\u0111\u0003\u0000\u0019\u0019"+
		"\u001d\u001d\u00df\u00df\u0002\u0000\\\\\u00ef\u00ef\u0005\u0000BBoo\u0095"+
		"\u0096\u00d5\u00d5\u010a\u010a\u0001\u0000\u0099\u009c\u0002\u0000aa\u00bb"+
		"\u00bb\u0003\u0000jj\u0081\u0081\u00e8\u00e8\u0004\u0000MM}}\u008c\u008c"+
		"\u00fd\u00fd\u0002\u0000\u00a9\u00a9\u0109\u0109\u0005\u000033GGxx\u00d8"+
		"\u00d8\u00f9\u00f9\u0002\u0000\u00ec\u00ec\u0100\u0100\u0002\u0000\u0120"+
		"\u0120\u0122\u0122\u0003\u0000EE\u0120\u0120\u0122\u01224\u0000\u0016"+
		"\u0019\u001b\u001b\u001d\u001e #&\'*02266?BDFHIKKMNQQSTWWZZ]accfjmmor"+
		"tuwwzz|}\u007f\u007f\u0081\u0083\u0085\u0085\u0087\u0087\u0089\u0089\u008c"+
		"\u0096\u0098\u009e\u00a2\u00a6\u00a8\u00ab\u00ae\u00ae\u00b0\u00bc\u00be"+
		"\u00c1\u00c3\u00ca\u00cc\u00ce\u00d0\u00d7\u00d9\u00e4\u00e6\u00e8\u00ea"+
		"\u00ee\u00f0\u00f2\u00f4\u00f5\u00f7\u00f7\u00f9\u00fb\u00fd\u00fd\u00ff"+
		"\u0101\u0104\u0104\u0106\u010b\u0c4e\u0000\u00c0\u0001\u0000\u0000\u0000"+
		"\u0002\u00c3\u0001\u0000\u0000\u0000\u0004\u00c6\u0001\u0000\u0000\u0000"+
		"\u0006\u00c9\u0001\u0000\u0000\u0000\b\u00cc\u0001\u0000\u0000\u0000\n"+
		"\u03e7\u0001\u0000\u0000\u0000\f\u03ea\u0001\u0000\u0000\u0000\u000e\u03ee"+
		"\u0001\u0000\u0000\u0000\u0010\u03fc\u0001\u0000\u0000\u0000\u0012\u03fe"+
		"\u0001\u0000\u0000\u0000\u0014\u040c\u0001\u0000\u0000\u0000\u0016\u0412"+
		"\u0001\u0000\u0000\u0000\u0018\u0416\u0001\u0000\u0000\u0000\u001a\u041e"+
		"\u0001\u0000\u0000\u0000\u001c\u0424\u0001\u0000\u0000\u0000\u001e\u0426"+
		"\u0001\u0000\u0000\u0000 \u045c\u0001\u0000\u0000\u0000\"\u0466\u0001"+
		"\u0000\u0000\u0000$\u0468\u0001\u0000\u0000\u0000&\u046a\u0001\u0000\u0000"+
		"\u0000(\u048e\u0001\u0000\u0000\u0000*\u0490\u0001\u0000\u0000\u0000,"+
		"\u0498\u0001\u0000\u0000\u0000.\u04c8\u0001\u0000\u0000\u00000\u04fa\u0001"+
		"\u0000\u0000\u00002\u0509\u0001\u0000\u0000\u00004\u050b\u0001\u0000\u0000"+
		"\u00006\u0512\u0001\u0000\u0000\u00008\u052f\u0001\u0000\u0000\u0000:"+
		"\u0538\u0001\u0000\u0000\u0000<\u0549\u0001\u0000\u0000\u0000>\u054b\u0001"+
		"\u0000\u0000\u0000@\u0572\u0001\u0000\u0000\u0000B\u0582\u0001\u0000\u0000"+
		"\u0000D\u0584\u0001\u0000\u0000\u0000F\u058d\u0001\u0000\u0000\u0000H"+
		"\u0595\u0001\u0000\u0000\u0000J\u059b\u0001\u0000\u0000\u0000L\u059d\u0001"+
		"\u0000\u0000\u0000N\u05f2\u0001\u0000\u0000\u0000P\u0601\u0001\u0000\u0000"+
		"\u0000R\u060c\u0001\u0000\u0000\u0000T\u0621\u0001\u0000\u0000\u0000V"+
		"\u0623\u0001\u0000\u0000\u0000X\u0630\u0001\u0000\u0000\u0000Z\u0634\u0001"+
		"\u0000\u0000\u0000\\\u063e\u0001\u0000\u0000\u0000^\u067e\u0001\u0000"+
		"\u0000\u0000`\u0680\u0001\u0000\u0000\u0000b\u0689\u0001\u0000\u0000\u0000"+
		"d\u06ee\u0001\u0000\u0000\u0000f\u06f0\u0001\u0000\u0000\u0000h\u0704"+
		"\u0001\u0000\u0000\u0000j\u0869\u0001\u0000\u0000\u0000l\u087f\u0001\u0000"+
		"\u0000\u0000n\u0885\u0001\u0000\u0000\u0000p\u088e\u0001\u0000\u0000\u0000"+
		"r\u0896\u0001\u0000\u0000\u0000t\u0898\u0001\u0000\u0000\u0000v\u089a"+
		"\u0001\u0000\u0000\u0000x\u089c\u0001\u0000\u0000\u0000z\u089e\u0001\u0000"+
		"\u0000\u0000|\u08a8\u0001\u0000\u0000\u0000~\u08aa\u0001\u0000\u0000\u0000"+
		"\u0080\u0907\u0001\u0000\u0000\u0000\u0082\u0919\u0001\u0000\u0000\u0000"+
		"\u0084\u091d\u0001\u0000\u0000\u0000\u0086\u091f\u0001\u0000\u0000\u0000"+
		"\u0088\u0924\u0001\u0000\u0000\u0000\u008a\u096a\u0001\u0000\u0000\u0000"+
		"\u008c\u096c\u0001\u0000\u0000\u0000\u008e\u097d\u0001\u0000\u0000\u0000"+
		"\u0090\u09bd\u0001\u0000\u0000\u0000\u0092\u09c8\u0001\u0000\u0000\u0000"+
		"\u0094\u09ca\u0001\u0000\u0000\u0000\u0096\u09f2\u0001\u0000\u0000\u0000"+
		"\u0098\u0a12\u0001\u0000\u0000\u0000\u009a\u0a14\u0001\u0000\u0000\u0000"+
		"\u009c\u0a1c\u0001\u0000\u0000\u0000\u009e\u0a23\u0001\u0000\u0000\u0000"+
		"\u00a0\u0a2c\u0001\u0000\u0000\u0000\u00a2\u0a33\u0001\u0000\u0000\u0000"+
		"\u00a4\u0a3a\u0001\u0000\u0000\u0000\u00a6\u0a3c\u0001\u0000\u0000\u0000"+
		"\u00a8\u0a44\u0001\u0000\u0000\u0000\u00aa\u0a46\u0001\u0000\u0000\u0000"+
		"\u00ac\u0a4e\u0001\u0000\u0000\u0000\u00ae\u0a54\u0001\u0000\u0000\u0000"+
		"\u00b0\u0a59\u0001\u0000\u0000\u0000\u00b2\u0a60\u0001\u0000\u0000\u0000"+
		"\u00b4\u0a62\u0001\u0000\u0000\u0000\u00b6\u0a6f\u0001\u0000\u0000\u0000"+
		"\u00b8\u0a7d\u0001\u0000\u0000\u0000\u00ba\u0a7f\u0001\u0000\u0000\u0000"+
		"\u00bc\u0a88\u0001\u0000\u0000\u0000\u00be\u0a8f\u0001\u0000\u0000\u0000"+
		"\u00c0\u00c1\u0003\n\u0005\u0000\u00c1\u00c2\u0005\u0000\u0000\u0001\u00c2"+
		"\u0001\u0001\u0000\u0000\u0000\u00c3\u00c4\u0003`0\u0000\u00c4\u00c5\u0005"+
		"\u0000\u0000\u0001\u00c5\u0003\u0001\u0000\u0000\u0000\u00c6\u00c7\u0003"+
		"\u00a6S\u0000\u00c7\u00c8\u0005\u0000\u0000\u0001\u00c8\u0005\u0001\u0000"+
		"\u0000\u0000\u00c9\u00ca\u0003\u0080@\u0000\u00ca\u00cb\u0005\u0000\u0000"+
		"\u0001\u00cb\u0007\u0001\u0000\u0000\u0000\u00cc\u00cd\u0003\u0094J\u0000"+
		"\u00cd\u00ce\u0005\u0000\u0000\u0001\u00ce\t\u0001\u0000\u0000\u0000\u00cf"+
		"\u03e8\u0003\f\u0006\u0000\u00d0\u00d1\u0005\u00fa\u0000\u0000\u00d1\u03e8"+
		"\u0003\u00b6[\u0000\u00d2\u00d3\u0005\u00fa\u0000\u0000\u00d3\u00d4\u0003"+
		"\u00b6[\u0000\u00d4\u00d5\u0005\u0001\u0000\u0000\u00d5\u00d6\u0003\u00b6"+
		"[\u0000\u00d6\u03e8\u0001\u0000\u0000\u0000\u00d7\u00d8\u00053\u0000\u0000"+
		"\u00d8\u00dc\u0005\u00d3\u0000\u0000\u00d9\u00da\u0005p\u0000\u0000\u00da"+
		"\u00db\u0005\u00a0\u0000\u0000\u00db\u00dd\u0005Y\u0000\u0000\u00dc\u00d9"+
		"\u0001\u0000\u0000\u0000\u00dc\u00dd\u0001\u0000\u0000\u0000\u00dd\u00de"+
		"\u0001\u0000\u0000\u0000\u00de\u00e1\u0003\u00aaU\u0000\u00df\u00e0\u0005"+
		"\"\u0000\u0000\u00e0\u00e2\u0003\u00b2Y\u0000\u00e1\u00df\u0001\u0000"+
		"\u0000\u0000\u00e1\u00e2\u0001\u0000\u0000\u0000\u00e2\u00e5\u0001\u0000"+
		"\u0000\u0000\u00e3\u00e4\u0005\u0105\u0000\u0000\u00e4\u00e6\u0003\u0016"+
		"\u000b\u0000\u00e5\u00e3\u0001\u0000\u0000\u0000\u00e5\u00e6\u0001\u0000"+
		"\u0000\u0000\u00e6\u03e8\u0001\u0000\u0000\u0000\u00e7\u00e8\u0005O\u0000"+
		"\u0000\u00e8\u00eb\u0005\u00d3\u0000\u0000\u00e9\u00ea\u0005p\u0000\u0000"+
		"\u00ea\u00ec\u0005Y\u0000\u0000\u00eb\u00e9\u0001\u0000\u0000\u0000\u00eb"+
		"\u00ec\u0001\u0000\u0000\u0000\u00ec\u00ed\u0001\u0000\u0000\u0000\u00ed"+
		"\u00ef\u0003\u00aaU\u0000\u00ee\u00f0\u0007\u0000\u0000\u0000\u00ef\u00ee"+
		"\u0001\u0000\u0000\u0000\u00ef\u00f0\u0001\u0000\u0000\u0000\u00f0\u03e8"+
		"\u0001\u0000\u0000\u0000\u00f1\u00f2\u0005\u001a\u0000\u0000\u00f2\u00f3"+
		"\u0005\u00d3\u0000\u0000\u00f3\u00f4\u0003\u00aaU\u0000\u00f4\u00f5\u0005"+
		"\u00c4\u0000\u0000\u00f5\u00f6\u0005\u00ed\u0000\u0000\u00f6\u00f7\u0003"+
		"\u00b6[\u0000\u00f7\u03e8\u0001\u0000\u0000\u0000\u00f8\u00f9\u0005\u001a"+
		"\u0000\u0000\u00f9\u00fa\u0005\u00d3\u0000\u0000\u00fa\u00fb\u0003\u00aa"+
		"U\u0000\u00fb\u00fc\u0005\u00dc\u0000\u0000\u00fc\u00fd\u0005\"\u0000"+
		"\u0000\u00fd\u00fe\u0003\u00b2Y\u0000\u00fe\u03e8\u0001\u0000\u0000\u0000"+
		"\u00ff\u0100\u00053\u0000\u0000\u0100\u0104\u0005\u00e5\u0000\u0000\u0101"+
		"\u0102\u0005p\u0000\u0000\u0102\u0103\u0005\u00a0\u0000\u0000\u0103\u0105"+
		"\u0005Y\u0000\u0000\u0104\u0101\u0001\u0000\u0000\u0000\u0104\u0105\u0001"+
		"\u0000\u0000\u0000\u0105\u0106\u0001\u0000\u0000\u0000\u0106\u0108\u0003"+
		"\u00aaU\u0000\u0107\u0109\u0003\\.\u0000\u0108\u0107\u0001\u0000\u0000"+
		"\u0000\u0108\u0109\u0001\u0000\u0000\u0000\u0109\u010c\u0001\u0000\u0000"+
		"\u0000\u010a\u010b\u0005.\u0000\u0000\u010b\u010d\u0003p8\u0000\u010c"+
		"\u010a\u0001\u0000\u0000\u0000\u010c\u010d\u0001\u0000\u0000\u0000\u010d"+
		"\u0110\u0001\u0000\u0000\u0000\u010e\u010f\u0005\u0105\u0000\u0000\u010f"+
		"\u0111\u0003\u0016\u000b\u0000\u0110\u010e\u0001\u0000\u0000\u0000\u0110"+
		"\u0111\u0001\u0000\u0000\u0000\u0111\u0112\u0001\u0000\u0000\u0000\u0112"+
		"\u0118\u0005\u001f\u0000\u0000\u0113\u0119\u0003\f\u0006\u0000\u0114\u0115"+
		"\u0005\u0002\u0000\u0000\u0115\u0116\u0003\f\u0006\u0000\u0116\u0117\u0005"+
		"\u0003\u0000\u0000\u0117\u0119\u0001\u0000\u0000\u0000\u0118\u0113\u0001"+
		"\u0000\u0000\u0000\u0118\u0114\u0001\u0000\u0000\u0000\u0119\u011f\u0001"+
		"\u0000\u0000\u0000\u011a\u011c\u0005\u0105\u0000\u0000\u011b\u011d\u0005"+
		"\u009d\u0000\u0000\u011c\u011b\u0001\u0000\u0000\u0000\u011c\u011d\u0001"+
		"\u0000\u0000\u0000\u011d\u011e\u0001\u0000\u0000\u0000\u011e\u0120\u0005"+
		"@\u0000\u0000\u011f\u011a\u0001\u0000\u0000\u0000\u011f\u0120\u0001\u0000"+
		"\u0000\u0000\u0120\u03e8\u0001\u0000\u0000\u0000\u0121\u0122\u00053\u0000"+
		"\u0000\u0122\u0126\u0005\u00e5\u0000\u0000\u0123\u0124\u0005p\u0000\u0000"+
		"\u0124\u0125\u0005\u00a0\u0000\u0000\u0125\u0127\u0005Y\u0000\u0000\u0126"+
		"\u0123\u0001\u0000\u0000\u0000\u0126\u0127\u0001\u0000\u0000\u0000\u0127"+
		"\u0128\u0001\u0000\u0000\u0000\u0128\u0129\u0003\u00aaU\u0000\u0129\u012a"+
		"\u0005\u0002\u0000\u0000\u012a\u012f\u0003\u0010\b\u0000\u012b\u012c\u0005"+
		"\u0004\u0000\u0000\u012c\u012e\u0003\u0010\b\u0000\u012d\u012b\u0001\u0000"+
		"\u0000\u0000\u012e\u0131\u0001\u0000\u0000\u0000\u012f\u012d\u0001\u0000"+
		"\u0000\u0000\u012f\u0130\u0001\u0000\u0000\u0000\u0130\u0132\u0001\u0000"+
		"\u0000\u0000\u0131\u012f\u0001\u0000\u0000\u0000\u0132\u0135\u0005\u0003"+
		"\u0000\u0000\u0133\u0134\u0005.\u0000\u0000\u0134\u0136\u0003p8\u0000"+
		"\u0135\u0133\u0001\u0000\u0000\u0000\u0135\u0136\u0001\u0000\u0000\u0000"+
		"\u0136\u0139\u0001\u0000\u0000\u0000\u0137\u0138\u0005\u0105\u0000\u0000"+
		"\u0138\u013a\u0003\u0016\u000b\u0000\u0139\u0137\u0001\u0000\u0000\u0000"+
		"\u0139\u013a\u0001\u0000\u0000\u0000\u013a\u03e8\u0001\u0000\u0000\u0000"+
		"\u013b\u013c\u0005O\u0000\u0000\u013c\u013f\u0005\u00e5\u0000\u0000\u013d"+
		"\u013e\u0005p\u0000\u0000\u013e\u0140\u0005Y\u0000\u0000\u013f\u013d\u0001"+
		"\u0000\u0000\u0000\u013f\u0140\u0001\u0000\u0000\u0000\u0140\u0141\u0001"+
		"\u0000\u0000\u0000\u0141\u03e8\u0003\u00aaU\u0000\u0142\u0143\u0005x\u0000"+
		"\u0000\u0143\u0144\u0005{\u0000\u0000\u0144\u0146\u0003\u00aaU\u0000\u0145"+
		"\u0147\u0003\\.\u0000\u0146\u0145\u0001\u0000\u0000\u0000\u0146\u0147"+
		"\u0001\u0000\u0000\u0000\u0147\u0148\u0001\u0000\u0000\u0000\u0148\u0149"+
		"\u0003\f\u0006\u0000\u0149\u03e8\u0001\u0000\u0000\u0000\u014a\u014b\u0005"+
		"G\u0000\u0000\u014b\u014c\u0005d\u0000\u0000\u014c\u014f\u0003\u00aaU"+
		"\u0000\u014d\u014e\u0005\u0103\u0000\u0000\u014e\u0150\u0003b1\u0000\u014f"+
		"\u014d\u0001\u0000\u0000\u0000\u014f\u0150\u0001\u0000\u0000\u0000\u0150"+
		"\u03e8\u0001\u0000\u0000\u0000\u0151\u0152\u0005\u00f0\u0000\u0000\u0152"+
		"\u0153\u0005\u00e5\u0000\u0000\u0153\u03e8\u0003\u00aaU\u0000\u0154\u0155"+
		"\u0005.\u0000\u0000\u0155\u0156\u0005\u00a7\u0000\u0000\u0156\u0157\u0005"+
		"\u00e5\u0000\u0000\u0157\u0158\u0003\u00aaU\u0000\u0158\u015b\u0005~\u0000"+
		"\u0000\u0159\u015c\u0003p8\u0000\u015a\u015c\u0005\u00a1\u0000\u0000\u015b"+
		"\u0159\u0001\u0000\u0000\u0000\u015b\u015a\u0001\u0000\u0000\u0000\u015c"+
		"\u03e8\u0001\u0000\u0000\u0000\u015d\u015e\u0005.\u0000\u0000\u015e\u015f"+
		"\u0005\u00a7\u0000\u0000\u015f\u0160\u0005,\u0000\u0000\u0160\u0161\u0003"+
		"\u00aaU\u0000\u0161\u0164\u0005~\u0000\u0000\u0162\u0165\u0003p8\u0000"+
		"\u0163\u0165\u0005\u00a1\u0000\u0000\u0164\u0162\u0001\u0000\u0000\u0000"+
		"\u0164\u0163\u0001\u0000\u0000\u0000\u0165\u03e8\u0001\u0000\u0000\u0000"+
		"\u0166\u0167\u0005\u001a\u0000\u0000\u0167\u016a\u0005\u00e5\u0000\u0000"+
		"\u0168\u0169\u0005p\u0000\u0000\u0169\u016b\u0005Y\u0000\u0000\u016a\u0168"+
		"\u0001\u0000\u0000\u0000\u016a\u016b\u0001\u0000\u0000\u0000\u016b\u016c"+
		"\u0001\u0000\u0000\u0000\u016c\u016d\u0003\u00aaU\u0000\u016d\u016e\u0005"+
		"\u00c4\u0000\u0000\u016e\u016f\u0005\u00ed\u0000\u0000\u016f\u0170\u0003"+
		"\u00aaU\u0000\u0170\u03e8\u0001\u0000\u0000\u0000\u0171\u0172\u0005\u001a"+
		"\u0000\u0000\u0172\u0175\u0005\u00e5\u0000\u0000\u0173\u0174\u0005p\u0000"+
		"\u0000\u0174\u0176\u0005Y\u0000\u0000\u0175\u0173\u0001\u0000\u0000\u0000"+
		"\u0175\u0176\u0001\u0000\u0000\u0000\u0176\u0177\u0001\u0000\u0000\u0000"+
		"\u0177\u0178\u0003\u00aaU\u0000\u0178\u0179\u0005\u0016\u0000\u0000\u0179"+
		"\u017d\u0005,\u0000\u0000\u017a\u017b\u0005p\u0000\u0000\u017b\u017c\u0005"+
		"\u00a0\u0000\u0000\u017c\u017e\u0005Y\u0000\u0000\u017d\u017a\u0001\u0000"+
		"\u0000\u0000\u017d\u017e\u0001\u0000\u0000\u0000\u017e\u017f\u0001\u0000"+
		"\u0000\u0000\u017f\u0180\u0003\u0012\t\u0000\u0180\u03e8\u0001\u0000\u0000"+
		"\u0000\u0181\u0182\u0005\u001a\u0000\u0000\u0182\u0185\u0005\u00e5\u0000"+
		"\u0000\u0183\u0184\u0005p\u0000\u0000\u0184\u0186\u0005Y\u0000\u0000\u0185"+
		"\u0183\u0001\u0000\u0000\u0000\u0185\u0186\u0001\u0000\u0000\u0000\u0186"+
		"\u0187\u0001\u0000\u0000\u0000\u0187\u0188\u0003\u00aaU\u0000\u0188\u0189"+
		"\u0005\u00c4\u0000\u0000\u0189\u018c\u0005,\u0000\u0000\u018a\u018b\u0005"+
		"p\u0000\u0000\u018b\u018d\u0005Y\u0000\u0000\u018c\u018a\u0001\u0000\u0000"+
		"\u0000\u018c\u018d\u0001\u0000\u0000\u0000\u018d\u018e\u0001\u0000\u0000"+
		"\u0000\u018e\u018f\u0003\u00b6[\u0000\u018f\u0190\u0005\u00ed\u0000\u0000"+
		"\u0190\u0191\u0003\u00b6[\u0000\u0191\u03e8\u0001\u0000\u0000\u0000\u0192"+
		"\u0193\u0005\u001a\u0000\u0000\u0193\u0196\u0005\u00e5\u0000\u0000\u0194"+
		"\u0195\u0005p\u0000\u0000\u0195\u0197\u0005Y\u0000\u0000\u0196\u0194\u0001"+
		"\u0000\u0000\u0000\u0196\u0197\u0001\u0000\u0000\u0000\u0197\u0198\u0001"+
		"\u0000\u0000\u0000\u0198\u0199\u0003\u00aaU\u0000\u0199\u019a\u0005O\u0000"+
		"\u0000\u019a\u019d\u0005,\u0000\u0000\u019b\u019c\u0005p\u0000\u0000\u019c"+
		"\u019e\u0005Y\u0000\u0000\u019d\u019b\u0001\u0000\u0000\u0000\u019d\u019e"+
		"\u0001\u0000\u0000\u0000\u019e\u019f\u0001\u0000\u0000\u0000\u019f\u01a0"+
		"\u0003\u00aaU\u0000\u01a0\u03e8\u0001\u0000\u0000\u0000\u01a1\u01a2\u0005"+
		"\u001a\u0000\u0000\u01a2\u01a3\u0005\u00e5\u0000\u0000\u01a3\u01a4\u0003"+
		"\u00aaU\u0000\u01a4\u01a5\u0005\u00dc\u0000\u0000\u01a5\u01a6\u0005\""+
		"\u0000\u0000\u01a6\u01a7\u0003\u00b2Y\u0000\u01a7\u03e8\u0001\u0000\u0000"+
		"\u0000\u01a8\u01a9\u0005\u001a\u0000\u0000\u01a9\u01aa\u0005\u00e5\u0000"+
		"\u0000\u01aa\u01ab\u0003\u00aaU\u0000\u01ab\u01ac\u0005\u00dc\u0000\u0000"+
		"\u01ac\u01ad\u0005\u00bf\u0000\u0000\u01ad\u01ae\u0003\u0018\f\u0000\u01ae"+
		"\u03e8\u0001\u0000\u0000\u0000\u01af\u01b0\u0005\u001a\u0000\u0000\u01b0"+
		"\u01b1\u0005\u00e5\u0000\u0000\u01b1\u01b2\u0003\u00aaU\u0000\u01b2\u01b3"+
		"\u0005X\u0000\u0000\u01b3\u01c0\u0003\u00b6[\u0000\u01b4\u01bd\u0005\u0002"+
		"\u0000\u0000\u01b5\u01ba\u0003\u00a2Q\u0000\u01b6\u01b7\u0005\u0004\u0000"+
		"\u0000\u01b7\u01b9\u0003\u00a2Q\u0000\u01b8\u01b6\u0001\u0000\u0000\u0000"+
		"\u01b9\u01bc\u0001\u0000\u0000\u0000\u01ba\u01b8\u0001\u0000\u0000\u0000"+
		"\u01ba\u01bb\u0001\u0000\u0000\u0000\u01bb\u01be\u0001\u0000\u0000\u0000"+
		"\u01bc\u01ba\u0001\u0000\u0000\u0000\u01bd\u01b5\u0001\u0000\u0000\u0000"+
		"\u01bd\u01be\u0001\u0000\u0000\u0000\u01be\u01bf\u0001\u0000\u0000\u0000"+
		"\u01bf\u01c1\u0005\u0003\u0000\u0000\u01c0\u01b4\u0001\u0000\u0000\u0000"+
		"\u01c0\u01c1\u0001\u0000\u0000\u0000\u01c1\u01c4\u0001\u0000\u0000\u0000"+
		"\u01c2\u01c3\u0005\u0103\u0000\u0000\u01c3\u01c5\u0003b1\u0000\u01c4\u01c2"+
		"\u0001\u0000\u0000\u0000\u01c4\u01c5\u0001\u0000\u0000\u0000\u01c5\u03e8"+
		"\u0001\u0000\u0000\u0000\u01c6\u01c7\u0005\u001b\u0000\u0000\u01c7\u01ca"+
		"\u0003\u00aaU\u0000\u01c8\u01c9\u0005\u0105\u0000\u0000\u01c9\u01cb\u0003"+
		"\u0016\u000b\u0000\u01ca\u01c8\u0001\u0000\u0000\u0000\u01ca\u01cb\u0001"+
		"\u0000\u0000\u0000\u01cb\u03e8\u0001\u0000\u0000\u0000\u01cc\u01cf\u0005"+
		"3\u0000\u0000\u01cd\u01ce\u0005\u00ac\u0000\u0000\u01ce\u01d0\u0005\u00c6"+
		"\u0000\u0000\u01cf\u01cd\u0001\u0000\u0000\u0000\u01cf\u01d0\u0001\u0000"+
		"\u0000\u0000\u01d0\u01d1\u0001\u0000\u0000\u0000\u01d1\u01d2\u0005\u0092"+
		"\u0000\u0000\u01d2\u01d6\u0005\u0101\u0000\u0000\u01d3\u01d4\u0005p\u0000"+
		"\u0000\u01d4\u01d5\u0005\u00a0\u0000\u0000\u01d5\u01d7\u0005Y\u0000\u0000"+
		"\u01d6\u01d3\u0001\u0000\u0000\u0000\u01d6\u01d7\u0001\u0000\u0000\u0000"+
		"\u01d7\u01d8\u0001\u0000\u0000\u0000\u01d8\u01db\u0003\u00aaU\u0000\u01d9"+
		"\u01da\u0005.\u0000\u0000\u01da\u01dc\u0003p8\u0000\u01db\u01d9\u0001"+
		"\u0000\u0000\u0000\u01db\u01dc\u0001\u0000\u0000\u0000\u01dc\u01df\u0001"+
		"\u0000\u0000\u0000\u01dd\u01de\u0005\u0105\u0000\u0000\u01de\u01e0\u0003"+
		"\u0016\u000b\u0000\u01df\u01dd\u0001\u0000\u0000\u0000\u01df\u01e0\u0001"+
		"\u0000\u0000\u0000\u01e0\u01e1\u0001\u0000\u0000\u0000\u01e1\u01e2\u0005"+
		"\u001f\u0000\u0000\u01e2\u01e3\u0003\f\u0006\u0000\u01e3\u03e8\u0001\u0000"+
		"\u0000\u0000\u01e4\u01e7\u00053\u0000\u0000\u01e5\u01e6\u0005\u00ac\u0000"+
		"\u0000\u01e6\u01e8\u0005\u00c6\u0000\u0000\u01e7\u01e5\u0001\u0000\u0000"+
		"\u0000\u01e7\u01e8\u0001\u0000\u0000\u0000\u01e8\u01e9\u0001\u0000\u0000"+
		"\u0000\u01e9\u01ea\u0005\u0101\u0000\u0000\u01ea\u01ed\u0003\u00aaU\u0000"+
		"\u01eb\u01ec\u0005.\u0000\u0000\u01ec\u01ee\u0003p8\u0000\u01ed\u01eb"+
		"\u0001\u0000\u0000\u0000\u01ed\u01ee\u0001\u0000\u0000\u0000\u01ee\u01f1"+
		"\u0001\u0000\u0000\u0000\u01ef\u01f0\u0005\u00d6\u0000\u0000\u01f0\u01f2"+
		"\u0007\u0001\u0000\u0000\u01f1\u01ef\u0001\u0000\u0000\u0000\u01f1\u01f2"+
		"\u0001\u0000\u0000\u0000\u01f2\u01f3\u0001\u0000\u0000\u0000\u01f3\u01f4"+
		"\u0005\u001f\u0000\u0000\u01f4\u01f5\u0003\f\u0006\u0000\u01f5\u03e8\u0001"+
		"\u0000\u0000\u0000\u01f6\u01f7\u0005\u00c3\u0000\u0000\u01f7\u01f8\u0005"+
		"\u0092\u0000\u0000\u01f8\u01f9\u0005\u0101\u0000\u0000\u01f9\u03e8\u0003"+
		"\u00aaU\u0000\u01fa\u01fb\u0005O\u0000\u0000\u01fb\u01fc\u0005\u0092\u0000"+
		"\u0000\u01fc\u01ff\u0005\u0101\u0000\u0000\u01fd\u01fe\u0005p\u0000\u0000"+
		"\u01fe\u0200\u0005Y\u0000\u0000\u01ff\u01fd\u0001\u0000\u0000\u0000\u01ff"+
		"\u0200\u0001\u0000\u0000\u0000\u0200\u0201\u0001\u0000\u0000\u0000\u0201"+
		"\u03e8\u0003\u00aaU\u0000\u0202\u0203\u0005\u001a\u0000\u0000\u0203\u0204"+
		"\u0005\u0092\u0000\u0000\u0204\u0207\u0005\u0101\u0000\u0000\u0205\u0206"+
		"\u0005p\u0000\u0000\u0206\u0208\u0005Y\u0000\u0000\u0207\u0205\u0001\u0000"+
		"\u0000\u0000\u0207\u0208\u0001\u0000\u0000\u0000\u0208\u0209\u0001\u0000"+
		"\u0000\u0000\u0209\u020a\u0003\u00aaU\u0000\u020a\u020b\u0005\u00c4\u0000"+
		"\u0000\u020b\u020c\u0005\u00ed\u0000\u0000\u020c\u020d\u0003\u00aaU\u0000"+
		"\u020d\u03e8\u0001\u0000\u0000\u0000\u020e\u020f\u0005\u001a\u0000\u0000"+
		"\u020f\u0210\u0005\u0092\u0000\u0000\u0210\u0211\u0005\u0101\u0000\u0000"+
		"\u0211\u0212\u0003\u00aaU\u0000\u0212\u0213\u0005\u00dc\u0000\u0000\u0213"+
		"\u0214\u0005\u00bf\u0000\u0000\u0214\u0215\u0003\u0018\f\u0000\u0215\u03e8"+
		"\u0001\u0000\u0000\u0000\u0216\u0217\u0005O\u0000\u0000\u0217\u021a\u0005"+
		"\u0101\u0000\u0000\u0218\u0219\u0005p\u0000\u0000\u0219\u021b\u0005Y\u0000"+
		"\u0000\u021a\u0218\u0001\u0000\u0000\u0000\u021a\u021b\u0001\u0000\u0000"+
		"\u0000\u021b\u021c\u0001\u0000\u0000\u0000\u021c\u03e8\u0003\u00aaU\u0000"+
		"\u021d\u021e\u0005\u001a\u0000\u0000\u021e\u021f\u0005\u0101\u0000\u0000"+
		"\u021f\u0220\u0003\u00aaU\u0000\u0220\u0221\u0005\u00c4\u0000\u0000\u0221"+
		"\u0222\u0005\u00ed\u0000\u0000\u0222\u0223\u0003\u00aaU\u0000\u0223\u03e8"+
		"\u0001\u0000\u0000\u0000\u0224\u0225\u0005\u001a\u0000\u0000\u0225\u0226"+
		"\u0005\u0101\u0000\u0000\u0226\u0227\u0003\u00aaU\u0000\u0227\u0228\u0005"+
		"\u00dc\u0000\u0000\u0228\u0229\u0005\"\u0000\u0000\u0229\u022a\u0003\u00b2"+
		"Y\u0000\u022a\u03e8\u0001\u0000\u0000\u0000\u022b\u022c\u0005&\u0000\u0000"+
		"\u022c\u022d\u0003\u00aaU\u0000\u022d\u0236\u0005\u0002\u0000\u0000\u022e"+
		"\u0233\u0003\u00a2Q\u0000\u022f\u0230\u0005\u0004\u0000\u0000\u0230\u0232"+
		"\u0003\u00a2Q\u0000\u0231\u022f\u0001\u0000\u0000\u0000\u0232\u0235\u0001"+
		"\u0000\u0000\u0000\u0233\u0231\u0001\u0000\u0000\u0000\u0233\u0234\u0001"+
		"\u0000\u0000\u0000\u0234\u0237\u0001\u0000\u0000\u0000\u0235\u0233\u0001"+
		"\u0000\u0000\u0000\u0236\u022e\u0001\u0000\u0000\u0000\u0236\u0237\u0001"+
		"\u0000\u0000\u0000\u0237\u0238\u0001\u0000\u0000\u0000\u0238\u0239\u0005"+
		"\u0003\u0000\u0000\u0239\u03e8\u0001\u0000\u0000\u0000\u023a\u023b\u0005"+
		"3\u0000\u0000\u023b\u023c\u0005\u00cc\u0000\u0000\u023c\u0240\u0003\u00b6"+
		"[\u0000\u023d\u023e\u0005\u0105\u0000\u0000\u023e\u023f\u0005\u0017\u0000"+
		"\u0000\u023f\u0241\u0003\u00b0X\u0000\u0240\u023d\u0001\u0000\u0000\u0000"+
		"\u0240\u0241\u0001\u0000\u0000\u0000\u0241\u0244\u0001\u0000\u0000\u0000"+
		"\u0242\u0243\u0005s\u0000\u0000\u0243\u0245\u0003\u00b6[\u0000\u0244\u0242"+
		"\u0001\u0000\u0000\u0000\u0244\u0245\u0001\u0000\u0000\u0000\u0245\u03e8"+
		"\u0001\u0000\u0000\u0000\u0246\u0247\u0005O\u0000\u0000\u0247\u0248\u0005"+
		"\u00cc\u0000\u0000\u0248\u024b\u0003\u00b6[\u0000\u0249\u024a\u0005s\u0000"+
		"\u0000\u024a\u024c\u0003\u00b6[\u0000\u024b\u0249\u0001\u0000\u0000\u0000"+
		"\u024b\u024c\u0001\u0000\u0000\u0000\u024c\u03e8\u0001\u0000\u0000\u0000"+
		"\u024d\u024e\u0005g\u0000\u0000\u024e\u024f\u0003\u00b4Z\u0000\u024f\u0250"+
		"\u0005\u00ed\u0000\u0000\u0250\u0255\u0003\u00b2Y\u0000\u0251\u0252\u0005"+
		"\u0004\u0000\u0000\u0252\u0254\u0003\u00b2Y\u0000\u0253\u0251\u0001\u0000"+
		"\u0000\u0000\u0254\u0257\u0001\u0000\u0000\u0000\u0255\u0253\u0001\u0000"+
		"\u0000\u0000\u0255\u0256\u0001\u0000\u0000\u0000\u0256\u025b\u0001\u0000"+
		"\u0000\u0000\u0257\u0255\u0001\u0000\u0000\u0000\u0258\u0259\u0005\u0105"+
		"\u0000\u0000\u0259\u025a\u0005\u0017\u0000\u0000\u025a\u025c\u0005\u00ab"+
		"\u0000\u0000\u025b\u0258\u0001\u0000\u0000\u0000\u025b\u025c\u0001\u0000"+
		"\u0000\u0000\u025c\u0260\u0001\u0000\u0000\u0000\u025d\u025e\u0005h\u0000"+
		"\u0000\u025e\u025f\u0005%\u0000\u0000\u025f\u0261\u0003\u00b0X\u0000\u0260"+
		"\u025d\u0001\u0000\u0000\u0000\u0260\u0261\u0001\u0000\u0000\u0000\u0261"+
		"\u0264\u0001\u0000\u0000\u0000\u0262\u0263\u0005s\u0000\u0000\u0263\u0265"+
		"\u0003\u00b6[\u0000\u0264\u0262\u0001\u0000\u0000\u0000\u0264\u0265\u0001"+
		"\u0000\u0000\u0000\u0265\u03e8\u0001\u0000\u0000\u0000\u0266\u026a\u0005"+
		"\u00ca\u0000\u0000\u0267\u0268\u0005\u0017\u0000\u0000\u0268\u0269\u0005"+
		"\u00ab\u0000\u0000\u0269\u026b\u0005b\u0000\u0000\u026a\u0267\u0001\u0000"+
		"\u0000\u0000\u026a\u026b\u0001\u0000\u0000\u0000\u026b\u026c\u0001\u0000"+
		"\u0000\u0000\u026c\u026d\u0003\u00b4Z\u0000\u026d\u026e\u0005d\u0000\u0000"+
		"\u026e\u0273\u0003\u00b2Y\u0000\u026f\u0270\u0005\u0004\u0000\u0000\u0270"+
		"\u0272\u0003\u00b2Y\u0000\u0271\u026f\u0001\u0000\u0000\u0000\u0272\u0275"+
		"\u0001\u0000\u0000\u0000\u0273\u0271\u0001\u0000\u0000\u0000\u0273\u0274"+
		"\u0001\u0000\u0000\u0000\u0274\u0279\u0001\u0000\u0000\u0000\u0275\u0273"+
		"\u0001\u0000\u0000\u0000\u0276\u0277\u0005h\u0000\u0000\u0277\u0278\u0005"+
		"%\u0000\u0000\u0278\u027a\u0003\u00b0X\u0000\u0279\u0276\u0001\u0000\u0000"+
		"\u0000\u0279\u027a\u0001\u0000\u0000\u0000\u027a\u027d\u0001\u0000\u0000"+
		"\u0000\u027b\u027c\u0005s\u0000\u0000\u027c\u027e\u0003\u00b6[\u0000\u027d"+
		"\u027b\u0001\u0000\u0000\u0000\u027d\u027e\u0001\u0000\u0000\u0000\u027e"+
		"\u03e8\u0001\u0000\u0000\u0000\u027f\u0280\u0005\u00dc\u0000\u0000\u0280"+
		"\u0284\u0005\u00cc\u0000\u0000\u0281\u0285\u0005\u0019\u0000\u0000\u0282"+
		"\u0285\u0005\u009e\u0000\u0000\u0283\u0285\u0003\u00b6[\u0000\u0284\u0281"+
		"\u0001\u0000\u0000\u0000\u0284\u0282\u0001\u0000\u0000\u0000\u0284\u0283"+
		"\u0001\u0000\u0000\u0000\u0285\u0288\u0001\u0000\u0000\u0000\u0286\u0287"+
		"\u0005s\u0000\u0000\u0287\u0289\u0003\u00b6[\u0000\u0288\u0286\u0001\u0000"+
		"\u0000\u0000\u0288\u0289\u0001\u0000\u0000\u0000\u0289\u03e8\u0001\u0000"+
		"\u0000\u0000\u028a\u0295\u0005g\u0000\u0000\u028b\u0290\u0003\u00a8T\u0000"+
		"\u028c\u028d\u0005\u0004\u0000\u0000\u028d\u028f\u0003\u00a8T\u0000\u028e"+
		"\u028c\u0001\u0000\u0000\u0000\u028f\u0292\u0001\u0000\u0000\u0000\u0290"+
		"\u028e\u0001\u0000\u0000\u0000\u0290\u0291\u0001\u0000\u0000\u0000\u0291"+
		"\u0296\u0001\u0000\u0000\u0000\u0292\u0290\u0001\u0000\u0000\u0000\u0293"+
		"\u0294\u0005\u0019\u0000\u0000\u0294\u0296\u0005\u00be\u0000\u0000\u0295"+
		"\u028b\u0001\u0000\u0000\u0000\u0295\u0293\u0001\u0000\u0000\u0000\u0296"+
		"\u0297\u0001\u0000\u0000\u0000\u0297\u0299\u0005\u00a7\u0000\u0000\u0298"+
		"\u029a\u0007\u0002\u0000\u0000\u0299\u0298\u0001\u0000\u0000\u0000\u0299"+
		"\u029a\u0001\u0000\u0000\u0000\u029a\u029b\u0001\u0000\u0000\u0000\u029b"+
		"\u029c\u0003\u00aaU\u0000\u029c\u029d\u0005\u00ed\u0000\u0000\u029d\u02a1"+
		"\u0003\u00b2Y\u0000\u029e\u029f\u0005\u0105\u0000\u0000\u029f\u02a0\u0005"+
		"g\u0000\u0000\u02a0\u02a2\u0005\u00ab\u0000\u0000\u02a1\u029e\u0001\u0000"+
		"\u0000\u0000\u02a1\u02a2\u0001\u0000\u0000\u0000\u02a2\u03e8\u0001\u0000"+
		"\u0000\u0000\u02a3\u02ae\u0005H\u0000\u0000\u02a4\u02a9\u0003\u00a8T\u0000"+
		"\u02a5\u02a6\u0005\u0004\u0000\u0000\u02a6\u02a8\u0003\u00a8T\u0000\u02a7"+
		"\u02a5\u0001\u0000\u0000\u0000\u02a8\u02ab\u0001\u0000\u0000\u0000\u02a9"+
		"\u02a7\u0001\u0000\u0000\u0000\u02a9\u02aa\u0001\u0000\u0000\u0000\u02aa"+
		"\u02af\u0001\u0000\u0000\u0000\u02ab\u02a9\u0001\u0000\u0000\u0000\u02ac"+
		"\u02ad\u0005\u0019\u0000\u0000\u02ad\u02af\u0005\u00be\u0000\u0000\u02ae"+
		"\u02a4\u0001\u0000\u0000\u0000\u02ae\u02ac\u0001\u0000\u0000\u0000\u02af"+
		"\u02b0\u0001\u0000\u0000\u0000\u02b0\u02b2\u0005\u00a7\u0000\u0000\u02b1"+
		"\u02b3\u0007\u0002\u0000\u0000\u02b2\u02b1\u0001\u0000\u0000\u0000\u02b2"+
		"\u02b3\u0001\u0000\u0000\u0000\u02b3\u02b4\u0001\u0000\u0000\u0000\u02b4"+
		"\u02b5\u0003\u00aaU\u0000\u02b5\u02b6\u0005\u00ed\u0000\u0000\u02b6\u02b7"+
		"\u0003\u00b2Y\u0000\u02b7\u03e8\u0001\u0000\u0000\u0000\u02b8\u02bc\u0005"+
		"\u00ca\u0000\u0000\u02b9\u02ba\u0005g\u0000\u0000\u02ba\u02bb\u0005\u00ab"+
		"\u0000\u0000\u02bb\u02bd\u0005b\u0000\u0000\u02bc\u02b9\u0001\u0000\u0000"+
		"\u0000\u02bc\u02bd\u0001\u0000\u0000\u0000\u02bd\u02c8\u0001\u0000\u0000"+
		"\u0000\u02be\u02c3\u0003\u00a8T\u0000\u02bf\u02c0\u0005\u0004\u0000\u0000"+
		"\u02c0\u02c2\u0003\u00a8T\u0000\u02c1\u02bf\u0001\u0000\u0000\u0000\u02c2"+
		"\u02c5\u0001\u0000\u0000\u0000\u02c3\u02c1\u0001\u0000\u0000\u0000\u02c3"+
		"\u02c4\u0001\u0000\u0000\u0000\u02c4\u02c9\u0001\u0000\u0000\u0000\u02c5"+
		"\u02c3\u0001\u0000\u0000\u0000\u02c6\u02c7\u0005\u0019\u0000\u0000\u02c7"+
		"\u02c9\u0005\u00be\u0000\u0000\u02c8\u02be\u0001\u0000\u0000\u0000\u02c8"+
		"\u02c6\u0001\u0000\u0000\u0000\u02c9\u02ca\u0001\u0000\u0000\u0000\u02ca"+
		"\u02cc\u0005\u00a7\u0000\u0000\u02cb\u02cd\u0007\u0002\u0000\u0000\u02cc"+
		"\u02cb\u0001\u0000\u0000\u0000\u02cc\u02cd\u0001\u0000\u0000\u0000\u02cd"+
		"\u02ce\u0001\u0000\u0000\u0000\u02ce\u02cf\u0003\u00aaU\u0000\u02cf\u02d0"+
		"\u0005d\u0000\u0000\u02d0\u02d1\u0003\u00b2Y\u0000\u02d1\u03e8\u0001\u0000"+
		"\u0000\u0000\u02d2\u02d3\u0005\u00de\u0000\u0000\u02d3\u02d9\u0005i\u0000"+
		"\u0000\u02d4\u02d6\u0005\u00a7\u0000\u0000\u02d5\u02d7\u0005\u00e5\u0000"+
		"\u0000\u02d6\u02d5\u0001\u0000\u0000\u0000\u02d6\u02d7\u0001\u0000\u0000"+
		"\u0000\u02d7\u02d8\u0001\u0000\u0000\u0000\u02d8\u02da\u0003\u00aaU\u0000"+
		"\u02d9\u02d4\u0001\u0000\u0000\u0000\u02d9\u02da\u0001\u0000\u0000\u0000"+
		"\u02da\u03e8\u0001\u0000\u0000\u0000\u02db\u02e7\u0005Z\u0000\u0000\u02dc"+
		"\u02dd\u0005\u0002\u0000\u0000\u02dd\u02e2\u0003\u009cN\u0000\u02de\u02df"+
		"\u0005\u0004\u0000\u0000\u02df\u02e1\u0003\u009cN\u0000\u02e0\u02de\u0001"+
		"\u0000\u0000\u0000\u02e1\u02e4\u0001\u0000\u0000\u0000\u02e2\u02e0\u0001"+
		"\u0000\u0000\u0000\u02e2\u02e3\u0001\u0000\u0000\u0000\u02e3\u02e5\u0001"+
		"\u0000\u0000\u0000\u02e4\u02e2\u0001\u0000\u0000\u0000\u02e5\u02e6\u0005"+
		"\u0003\u0000\u0000\u02e6\u02e8\u0001\u0000\u0000\u0000\u02e7\u02dc\u0001"+
		"\u0000\u0000\u0000\u02e7\u02e8\u0001\u0000\u0000\u0000\u02e8\u02e9\u0001"+
		"\u0000\u0000\u0000\u02e9\u03e8\u0003\n\u0005\u0000\u02ea\u02eb\u0005Z"+
		"\u0000\u0000\u02eb\u02ed\u0005\u001b\u0000\u0000\u02ec\u02ee\u0005\u00ff"+
		"\u0000\u0000\u02ed\u02ec\u0001\u0000\u0000\u0000\u02ed\u02ee\u0001\u0000"+
		"\u0000\u0000\u02ee\u02ef\u0001\u0000\u0000\u0000\u02ef\u03e8\u0003\n\u0005"+
		"\u0000\u02f0\u02f1\u0005\u00de\u0000\u0000\u02f1\u02f2\u00053\u0000\u0000"+
		"\u02f2\u02f3\u0005\u00e5\u0000\u0000\u02f3\u03e8\u0003\u00aaU\u0000\u02f4"+
		"\u02f5\u0005\u00de\u0000\u0000\u02f5\u02f6\u00053\u0000\u0000\u02f6\u02f7"+
		"\u0005\u00d3\u0000\u0000\u02f7\u03e8\u0003\u00aaU\u0000\u02f8\u02f9\u0005"+
		"\u00de\u0000\u0000\u02f9\u02fa\u00053\u0000\u0000\u02fa\u02fb\u0005\u0101"+
		"\u0000\u0000\u02fb\u03e8\u0003\u00aaU\u0000\u02fc\u02fd\u0005\u00de\u0000"+
		"\u0000\u02fd\u02fe\u00053\u0000\u0000\u02fe\u02ff\u0005\u0092\u0000\u0000"+
		"\u02ff\u0300\u0005\u0101\u0000\u0000\u0300\u03e8\u0003\u00aaU\u0000\u0301"+
		"\u0302\u0005\u00de\u0000\u0000\u0302\u0305\u0005\u00e6\u0000\u0000\u0303"+
		"\u0304\u0007\u0003\u0000\u0000\u0304\u0306\u0003\u00aaU\u0000\u0305\u0303"+
		"\u0001\u0000\u0000\u0000\u0305\u0306\u0001\u0000\u0000\u0000\u0306\u030d"+
		"\u0001\u0000\u0000\u0000\u0307\u0308\u0005\u0086\u0000\u0000\u0308\u030b"+
		"\u0003p8\u0000\u0309\u030a\u0005U\u0000\u0000\u030a\u030c\u0003p8\u0000"+
		"\u030b\u0309\u0001\u0000\u0000\u0000\u030b\u030c\u0001\u0000\u0000\u0000"+
		"\u030c\u030e\u0001\u0000\u0000\u0000\u030d\u0307\u0001\u0000\u0000\u0000"+
		"\u030d\u030e\u0001\u0000\u0000\u0000\u030e\u03e8\u0001\u0000\u0000\u0000"+
		"\u030f\u0310\u0005\u00de\u0000\u0000\u0310\u0313\u0005\u00d4\u0000\u0000"+
		"\u0311\u0312\u0007\u0003\u0000\u0000\u0312\u0314\u0003\u00b6[\u0000\u0313"+
		"\u0311\u0001\u0000\u0000\u0000\u0313\u0314\u0001\u0000\u0000\u0000\u0314"+
		"\u031b\u0001\u0000\u0000\u0000\u0315\u0316\u0005\u0086\u0000\u0000\u0316"+
		"\u0319\u0003p8\u0000\u0317\u0318\u0005U\u0000\u0000\u0318\u031a\u0003"+
		"p8\u0000\u0319\u0317\u0001\u0000\u0000\u0000\u0319\u031a\u0001\u0000\u0000"+
		"\u0000\u031a\u031c\u0001\u0000\u0000\u0000\u031b\u0315\u0001\u0000\u0000"+
		"\u0000\u031b\u031c\u0001\u0000\u0000\u0000\u031c\u03e8\u0001\u0000\u0000"+
		"\u0000\u031d\u031e\u0005\u00de\u0000\u0000\u031e\u0325\u0005*\u0000\u0000"+
		"\u031f\u0320\u0005\u0086\u0000\u0000\u0320\u0323\u0003p8\u0000\u0321\u0322"+
		"\u0005U\u0000\u0000\u0322\u0324\u0003p8\u0000\u0323\u0321\u0001\u0000"+
		"\u0000\u0000\u0323\u0324\u0001\u0000\u0000\u0000\u0324\u0326\u0001\u0000"+
		"\u0000\u0000\u0325\u031f\u0001\u0000\u0000\u0000\u0325\u0326\u0001\u0000"+
		"\u0000\u0000\u0326\u03e8\u0001\u0000\u0000\u0000\u0327\u0328\u0005\u00de"+
		"\u0000\u0000\u0328\u0329\u0005-\u0000\u0000\u0329\u032b\u0007\u0003\u0000"+
		"\u0000\u032a\u032c\u0003\u00aaU\u0000\u032b\u032a\u0001\u0000\u0000\u0000"+
		"\u032b\u032c\u0001\u0000\u0000\u0000\u032c\u0333\u0001\u0000\u0000\u0000"+
		"\u032d\u032e\u0005\u0086\u0000\u0000\u032e\u0331\u0003p8\u0000\u032f\u0330"+
		"\u0005U\u0000\u0000\u0330\u0332\u0003p8\u0000\u0331\u032f\u0001\u0000"+
		"\u0000\u0000\u0331\u0332\u0001\u0000\u0000\u0000\u0332\u0334\u0001\u0000"+
		"\u0000\u0000\u0333\u032d\u0001\u0000\u0000\u0000\u0333\u0334\u0001\u0000"+
		"\u0000\u0000\u0334\u03e8\u0001\u0000\u0000\u0000\u0335\u0336\u0005\u00de"+
		"\u0000\u0000\u0336\u0337\u0005\u00e1\u0000\u0000\u0337\u0338\u0005b\u0000"+
		"\u0000\u0338\u03e8\u0003\u00aaU\u0000\u0339\u033a\u0005\u00de\u0000\u0000"+
		"\u033a\u033b\u0005\u00e1\u0000\u0000\u033b\u033c\u0005b\u0000\u0000\u033c"+
		"\u033d\u0005\u0002\u0000\u0000\u033d\u033e\u0003\f\u0006\u0000\u033e\u033f"+
		"\u0005\u0003\u0000\u0000\u033f\u03e8\u0001\u0000\u0000\u0000\u0340\u0342"+
		"\u0005\u00de\u0000\u0000\u0341\u0343\u00056\u0000\u0000\u0342\u0341\u0001"+
		"\u0000\u0000\u0000\u0342\u0343\u0001\u0000\u0000\u0000\u0343\u0344\u0001"+
		"\u0000\u0000\u0000\u0344\u0347\u0005\u00cd\u0000\u0000\u0345\u0346\u0007"+
		"\u0003\u0000\u0000\u0346\u0348\u0003\u00b6[\u0000\u0347\u0345\u0001\u0000"+
		"\u0000\u0000\u0347\u0348\u0001\u0000\u0000\u0000\u0348\u03e8\u0001\u0000"+
		"\u0000\u0000\u0349\u034a\u0005\u00de\u0000\u0000\u034a\u034b\u0005\u00cc"+
		"\u0000\u0000\u034b\u034e\u0005i\u0000\u0000\u034c\u034d\u0007\u0003\u0000"+
		"\u0000\u034d\u034f\u0003\u00b6[\u0000\u034e\u034c\u0001\u0000\u0000\u0000"+
		"\u034e\u034f\u0001\u0000\u0000\u0000\u034f\u03e8\u0001\u0000\u0000\u0000"+
		"\u0350\u0351\u0005J\u0000\u0000\u0351\u03e8\u0003\u00aaU\u0000\u0352\u0353"+
		"\u0005I\u0000\u0000\u0353\u03e8\u0003\u00aaU\u0000\u0354\u0355\u0005\u00de"+
		"\u0000\u0000\u0355\u035c\u0005f\u0000\u0000\u0356\u0357\u0005\u0086\u0000"+
		"\u0000\u0357\u035a\u0003p8\u0000\u0358\u0359\u0005U\u0000\u0000\u0359"+
		"\u035b\u0003p8\u0000\u035a\u0358\u0001\u0000\u0000\u0000\u035a\u035b\u0001"+
		"\u0000\u0000\u0000\u035b\u035d\u0001\u0000\u0000\u0000\u035c\u0356\u0001"+
		"\u0000\u0000\u0000\u035c\u035d\u0001\u0000\u0000\u0000\u035d\u03e8\u0001"+
		"\u0000\u0000\u0000\u035e\u035f\u0005\u00de\u0000\u0000\u035f\u0366\u0005"+
		"\u00da\u0000\u0000\u0360\u0361\u0005\u0086\u0000\u0000\u0361\u0364\u0003"+
		"p8\u0000\u0362\u0363\u0005U\u0000\u0000\u0363\u0365\u0003p8\u0000\u0364"+
		"\u0362\u0001\u0000\u0000\u0000\u0364\u0365\u0001\u0000\u0000\u0000\u0365"+
		"\u0367\u0001\u0000\u0000\u0000\u0366\u0360\u0001\u0000\u0000\u0000\u0366"+
		"\u0367\u0001\u0000\u0000\u0000\u0367\u03e8\u0001\u0000\u0000\u0000\u0368"+
		"\u0369\u0005\u00dc\u0000\u0000\u0369\u036a\u0005\u00da\u0000\u0000\u036a"+
		"\u036b\u0003\u00aaU\u0000\u036b\u036c\u0005\u010c\u0000\u0000\u036c\u036d"+
		"\u0003`0\u0000\u036d\u03e8\u0001\u0000\u0000\u0000\u036e\u036f\u0005\u00c7"+
		"\u0000\u0000\u036f\u0370\u0005\u00da\u0000\u0000\u0370\u03e8\u0003\u00aa"+
		"U\u0000\u0371\u0372\u0005\u00e0\u0000\u0000\u0372\u037b\u0005\u00ee\u0000"+
		"\u0000\u0373\u0378\u0003\u009eO\u0000\u0374\u0375\u0005\u0004\u0000\u0000"+
		"\u0375\u0377\u0003\u009eO\u0000\u0376\u0374\u0001\u0000\u0000\u0000\u0377"+
		"\u037a\u0001\u0000\u0000\u0000\u0378\u0376\u0001\u0000\u0000\u0000\u0378"+
		"\u0379\u0001\u0000\u0000\u0000\u0379\u037c\u0001\u0000\u0000\u0000\u037a"+
		"\u0378\u0001\u0000\u0000\u0000\u037b\u0373\u0001\u0000\u0000\u0000\u037b"+
		"\u037c\u0001\u0000\u0000\u0000\u037c\u03e8\u0001\u0000\u0000\u0000\u037d"+
		"\u037f\u0005/\u0000\u0000\u037e\u0380\u0005\u0108\u0000\u0000\u037f\u037e"+
		"\u0001\u0000\u0000\u0000\u037f\u0380\u0001\u0000\u0000\u0000\u0380\u03e8"+
		"\u0001\u0000\u0000\u0000\u0381\u0383\u0005\u00ce\u0000\u0000\u0382\u0384"+
		"\u0005\u0108\u0000\u0000\u0383\u0382\u0001\u0000\u0000\u0000\u0383\u0384"+
		"\u0001\u0000\u0000\u0000\u0384\u03e8\u0001\u0000\u0000\u0000\u0385\u0386"+
		"\u0005\u00bd\u0000\u0000\u0386\u0387\u0003\u00b6[\u0000\u0387\u0388\u0005"+
		"d\u0000\u0000\u0388\u0389\u0003\n\u0005\u0000\u0389\u03e8\u0001\u0000"+
		"\u0000\u0000\u038a\u038b\u0005C\u0000\u0000\u038b\u038c\u0005\u00bd\u0000"+
		"\u0000\u038c\u03e8\u0003\u00b6[\u0000\u038d\u038e\u0005X\u0000\u0000\u038e"+
		"\u0398\u0003\u00b6[\u0000\u038f\u0390\u0005\u00fc\u0000\u0000\u0390\u0395"+
		"\u0003`0\u0000\u0391\u0392\u0005\u0004\u0000\u0000\u0392\u0394\u0003`"+
		"0\u0000\u0393\u0391\u0001\u0000\u0000\u0000\u0394\u0397\u0001\u0000\u0000"+
		"\u0000\u0395\u0393\u0001\u0000\u0000\u0000\u0395\u0396\u0001\u0000\u0000"+
		"\u0000\u0396\u0399\u0001\u0000\u0000\u0000\u0397\u0395\u0001\u0000\u0000"+
		"\u0000\u0398\u038f\u0001\u0000\u0000\u0000\u0398\u0399\u0001\u0000\u0000"+
		"\u0000\u0399\u03e8\u0001\u0000\u0000\u0000\u039a\u039b\u0005J\u0000\u0000"+
		"\u039b\u039c\u0005w\u0000\u0000\u039c\u03e8\u0003\u00b6[\u0000\u039d\u039e"+
		"\u0005J\u0000\u0000\u039e\u039f\u0005\u00b0\u0000\u0000\u039f\u03e8\u0003"+
		"\u00b6[\u0000\u03a0\u03a1\u0005\u00dc\u0000\u0000\u03a1\u03a2\u0005\u00b6"+
		"\u0000\u0000\u03a2\u03e8\u0003\u00a6S\u0000\u03a3\u03a4\u0005\u00dc\u0000"+
		"\u0000\u03a4\u03a5\u0005\u00eb\u0000\u0000\u03a5\u03a8\u0005\u010b\u0000"+
		"\u0000\u03a6\u03a9\u0005\u0089\u0000\u0000\u03a7\u03a9\u0003`0\u0000\u03a8"+
		"\u03a6\u0001\u0000\u0000\u0000\u03a8\u03a7\u0001\u0000\u0000\u0000\u03a9"+
		"\u03e8\u0001\u0000\u0000\u0000\u03aa\u03ab\u0005\u00f9\u0000\u0000\u03ab"+
		"\u03ac\u0003\u00aaU\u0000\u03ac\u03ad\u0005\u00dc\u0000\u0000\u03ad\u03b2"+
		"\u0003\u009aM\u0000\u03ae\u03af\u0005\u0004\u0000\u0000\u03af\u03b1\u0003"+
		"\u009aM\u0000\u03b0\u03ae\u0001\u0000\u0000\u0000\u03b1\u03b4\u0001\u0000"+
		"\u0000\u0000\u03b2\u03b0\u0001\u0000\u0000\u0000\u03b2\u03b3\u0001\u0000"+
		"\u0000\u0000\u03b3\u03b7\u0001\u0000\u0000\u0000\u03b4\u03b2\u0001\u0000"+
		"\u0000\u0000\u03b5\u03b6\u0005\u0103\u0000\u0000\u03b6\u03b8\u0003b1\u0000"+
		"\u03b7\u03b5\u0001\u0000\u0000\u0000\u03b7\u03b8\u0001\u0000\u0000\u0000"+
		"\u03b8\u03e8\u0001\u0000\u0000\u0000\u03b9\u03ba\u0005\u0094\u0000\u0000"+
		"\u03ba\u03bb\u0005{\u0000\u0000\u03bb\u03c0\u0003\u00aaU\u0000\u03bc\u03be"+
		"\u0005\u001f\u0000\u0000\u03bd\u03bc\u0001\u0000\u0000\u0000\u03bd\u03be"+
		"\u0001\u0000\u0000\u0000\u03be\u03bf\u0001\u0000\u0000\u0000\u03bf\u03c1"+
		"\u0003\u00b6[\u0000\u03c0\u03bd\u0001\u0000\u0000\u0000\u03c0\u03c1\u0001"+
		"\u0000\u0000\u0000\u03c1\u03c2\u0001\u0000\u0000\u0000\u03c2\u03c3\u0005"+
		"\u00fc\u0000\u0000\u03c3\u03c4\u0003>\u001f\u0000\u03c4\u03c5\u0005\u00a7"+
		"\u0000\u0000\u03c5\u03c7\u0003`0\u0000\u03c6\u03c8\u0003\u008aE\u0000"+
		"\u03c7\u03c6\u0001\u0000\u0000\u0000\u03c8\u03c9\u0001\u0000\u0000\u0000"+
		"\u03c9\u03c7\u0001\u0000\u0000\u0000\u03c9\u03ca\u0001\u0000\u0000\u0000"+
		"\u03ca\u03e8\u0001\u0000\u0000\u0000\u03cb\u03cc\u0005D\u0000\u0000\u03cc"+
		"\u03ce\u0003\u00b6[\u0000\u03cd\u03cf\u0005\u0005\u0000\u0000\u03ce\u03cd"+
		"\u0001\u0000\u0000\u0000\u03ce\u03cf\u0001\u0000\u0000\u0000\u03cf\u03d1"+
		"\u0001\u0000\u0000\u0000\u03d0\u03d2\u0007\u0004\u0000\u0000\u03d1\u03d0"+
		"\u0001\u0000\u0000\u0000\u03d1\u03d2\u0001\u0000\u0000\u0000\u03d2\u03d7"+
		"\u0001\u0000\u0000\u0000\u03d3\u03d5\u0005\u009d\u0000\u0000\u03d4\u03d3"+
		"\u0001\u0000\u0000\u0000\u03d4\u03d5\u0001\u0000\u0000\u0000\u03d5\u03d6"+
		"\u0001\u0000\u0000\u0000\u03d6\u03d8\u0005\b\u0000\u0000\u03d7\u03d4\u0001"+
		"\u0000\u0000\u0000\u03d7\u03d8\u0001\u0000\u0000\u0000\u03d8\u03d9\u0001"+
		"\u0000\u0000\u0000\u03d9\u03dc\u0005?\u0000\u0000\u03da\u03db\u0007\u0005"+
		"\u0000\u0000\u03db\u03dd\u0005\t\u0000\u0000\u03dc\u03da\u0001\u0000\u0000"+
		"\u0000\u03dc\u03dd\u0001\u0000\u0000\u0000\u03dd\u03de\u0001\u0000\u0000"+
		"\u0000\u03de\u03df\u0005b\u0000\u0000\u03df\u03e0\u0003\f\u0006\u0000"+
		"\u03e0\u03e8\u0001\u0000\u0000\u0000\u03e1\u03e2\u0005]\u0000\u0000\u03e2"+
		"\u03e3\u0005\u011d\u0000\u0000\u03e3\u03e4\u0007\u0003\u0000\u0000\u03e4"+
		"\u03e8\u0003\u00b6[\u0000\u03e5\u03e6\u0005r\u0000\u0000\u03e6\u03e8\u0003"+
		"`0\u0000\u03e7\u00cf\u0001\u0000\u0000\u0000\u03e7\u00d0\u0001\u0000\u0000"+
		"\u0000\u03e7\u00d2\u0001\u0000\u0000\u0000\u03e7\u00d7\u0001\u0000\u0000"+
		"\u0000\u03e7\u00e7\u0001\u0000\u0000\u0000\u03e7\u00f1\u0001\u0000\u0000"+
		"\u0000\u03e7\u00f8\u0001\u0000\u0000\u0000\u03e7\u00ff\u0001\u0000\u0000"+
		"\u0000\u03e7\u0121\u0001\u0000\u0000\u0000\u03e7\u013b\u0001\u0000\u0000"+
		"\u0000\u03e7\u0142\u0001\u0000\u0000\u0000\u03e7\u014a\u0001\u0000\u0000"+
		"\u0000\u03e7\u0151\u0001\u0000\u0000\u0000\u03e7\u0154\u0001\u0000\u0000"+
		"\u0000\u03e7\u015d\u0001\u0000\u0000\u0000\u03e7\u0166\u0001\u0000\u0000"+
		"\u0000\u03e7\u0171\u0001\u0000\u0000\u0000\u03e7\u0181\u0001\u0000\u0000"+
		"\u0000\u03e7\u0192\u0001\u0000\u0000\u0000\u03e7\u01a1\u0001\u0000\u0000"+
		"\u0000\u03e7\u01a8\u0001\u0000\u0000\u0000\u03e7\u01af\u0001\u0000\u0000"+
		"\u0000\u03e7\u01c6\u0001\u0000\u0000\u0000\u03e7\u01cc\u0001\u0000\u0000"+
		"\u0000\u03e7\u01e4\u0001\u0000\u0000\u0000\u03e7\u01f6\u0001\u0000\u0000"+
		"\u0000\u03e7\u01fa\u0001\u0000\u0000\u0000\u03e7\u0202\u0001\u0000\u0000"+
		"\u0000\u03e7\u020e\u0001\u0000\u0000\u0000\u03e7\u0216\u0001\u0000\u0000"+
		"\u0000\u03e7\u021d\u0001\u0000\u0000\u0000\u03e7\u0224\u0001\u0000\u0000"+
		"\u0000\u03e7\u022b\u0001\u0000\u0000\u0000\u03e7\u023a\u0001\u0000\u0000"+
		"\u0000\u03e7\u0246\u0001\u0000\u0000\u0000\u03e7\u024d\u0001\u0000\u0000"+
		"\u0000\u03e7\u0266\u0001\u0000\u0000\u0000\u03e7\u027f\u0001\u0000\u0000"+
		"\u0000\u03e7\u028a\u0001\u0000\u0000\u0000\u03e7\u02a3\u0001\u0000\u0000"+
		"\u0000\u03e7\u02b8\u0001\u0000\u0000\u0000\u03e7\u02d2\u0001\u0000\u0000"+
		"\u0000\u03e7\u02db\u0001\u0000\u0000\u0000\u03e7\u02ea\u0001\u0000\u0000"+
		"\u0000\u03e7\u02f0\u0001\u0000\u0000\u0000\u03e7\u02f4\u0001\u0000\u0000"+
		"\u0000\u03e7\u02f8\u0001\u0000\u0000\u0000\u03e7\u02fc\u0001\u0000\u0000"+
		"\u0000\u03e7\u0301\u0001\u0000\u0000\u0000\u03e7\u030f\u0001\u0000\u0000"+
		"\u0000\u03e7\u031d\u0001\u0000\u0000\u0000\u03e7\u0327\u0001\u0000\u0000"+
		"\u0000\u03e7\u0335\u0001\u0000\u0000\u0000\u03e7\u0339\u0001\u0000\u0000"+
		"\u0000\u03e7\u0340\u0001\u0000\u0000\u0000\u03e7\u0349\u0001\u0000\u0000"+
		"\u0000\u03e7\u0350\u0001\u0000\u0000\u0000\u03e7\u0352\u0001\u0000\u0000"+
		"\u0000\u03e7\u0354\u0001\u0000\u0000\u0000\u03e7\u035e\u0001\u0000\u0000"+
		"\u0000\u03e7\u0368\u0001\u0000\u0000\u0000\u03e7\u036e\u0001\u0000\u0000"+
		"\u0000\u03e7\u0371\u0001\u0000\u0000\u0000\u03e7\u037d\u0001\u0000\u0000"+
		"\u0000\u03e7\u0381\u0001\u0000\u0000\u0000\u03e7\u0385\u0001\u0000\u0000"+
		"\u0000\u03e7\u038a\u0001\u0000\u0000\u0000\u03e7\u038d\u0001\u0000\u0000"+
		"\u0000\u03e7\u039a\u0001\u0000\u0000\u0000\u03e7\u039d\u0001\u0000\u0000"+
		"\u0000\u03e7\u03a0\u0001\u0000\u0000\u0000\u03e7\u03a3\u0001\u0000\u0000"+
		"\u0000\u03e7\u03aa\u0001\u0000\u0000\u0000\u03e7\u03b9\u0001\u0000\u0000"+
		"\u0000\u03e7\u03cb\u0001\u0000\u0000\u0000\u03e7\u03e1\u0001\u0000\u0000"+
		"\u0000\u03e7\u03e5\u0001\u0000\u0000\u0000\u03e8\u000b\u0001\u0000\u0000"+
		"\u0000\u03e9\u03eb\u0003\u000e\u0007\u0000\u03ea\u03e9\u0001\u0000\u0000"+
		"\u0000\u03ea\u03eb\u0001\u0000\u0000\u0000\u03eb\u03ec\u0001\u0000\u0000"+
		"\u0000\u03ec\u03ed\u0003\u001e\u000f\u0000\u03ed\r\u0001\u0000\u0000\u0000"+
		"\u03ee\u03f0\u0005\u0105\u0000\u0000\u03ef\u03f1\u0005\u00c2\u0000\u0000"+
		"\u03f0\u03ef\u0001\u0000\u0000\u0000\u03f0\u03f1\u0001\u0000\u0000\u0000"+
		"\u03f1\u03f2\u0001\u0000\u0000\u0000\u03f2\u03f7\u00038\u001c\u0000\u03f3"+
		"\u03f4\u0005\u0004\u0000\u0000\u03f4\u03f6\u00038\u001c\u0000\u03f5\u03f3"+
		"\u0001\u0000\u0000\u0000\u03f6\u03f9\u0001\u0000\u0000\u0000\u03f7\u03f5"+
		"\u0001\u0000\u0000\u0000\u03f7\u03f8\u0001\u0000\u0000\u0000\u03f8\u000f"+
		"\u0001\u0000\u0000\u0000\u03f9\u03f7\u0001\u0000\u0000\u0000\u03fa\u03fd"+
		"\u0003\u0012\t\u0000\u03fb\u03fd\u0003\u0014\n\u0000\u03fc\u03fa\u0001"+
		"\u0000\u0000\u0000\u03fc\u03fb\u0001\u0000\u0000\u0000\u03fd\u0011\u0001"+
		"\u0000\u0000\u0000\u03fe\u03ff\u0003\u00b6[\u0000\u03ff\u0402\u0003\u0080"+
		"@\u0000\u0400\u0401\u0005\u00a0\u0000\u0000\u0401\u0403\u0005\u00a1\u0000"+
		"\u0000\u0402\u0400\u0001\u0000\u0000\u0000\u0402\u0403\u0001\u0000\u0000"+
		"\u0000\u0403\u0406\u0001\u0000\u0000\u0000\u0404\u0405\u0005.\u0000\u0000"+
		"\u0405\u0407\u0003p8\u0000\u0406\u0404\u0001\u0000\u0000\u0000\u0406\u0407"+
		"\u0001\u0000\u0000\u0000\u0407\u040a\u0001\u0000\u0000\u0000\u0408\u0409"+
		"\u0005\u0105\u0000\u0000\u0409\u040b\u0003\u0016\u000b\u0000\u040a\u0408"+
		"\u0001\u0000\u0000\u0000\u040a\u040b\u0001\u0000\u0000\u0000\u040b\u0013"+
		"\u0001\u0000\u0000\u0000\u040c\u040d\u0005\u0086\u0000\u0000\u040d\u0410"+
		"\u0003\u00aaU\u0000\u040e\u040f\u0007\u0006\u0000\u0000\u040f\u0411\u0005"+
		"\u00bf\u0000\u0000\u0410\u040e\u0001\u0000\u0000\u0000\u0410\u0411\u0001"+
		"\u0000\u0000\u0000\u0411\u0015\u0001\u0000\u0000\u0000\u0412\u0413\u0005"+
		"\u0002\u0000\u0000\u0413\u0414\u0003\u0018\f\u0000\u0414\u0415\u0005\u0003"+
		"\u0000\u0000\u0415\u0017\u0001\u0000\u0000\u0000\u0416\u041b\u0003\u001a"+
		"\r\u0000\u0417\u0418\u0005\u0004\u0000\u0000\u0418\u041a\u0003\u001a\r"+
		"\u0000\u0419\u0417\u0001\u0000\u0000\u0000\u041a\u041d\u0001\u0000\u0000"+
		"\u0000\u041b\u0419\u0001\u0000\u0000\u0000\u041b\u041c\u0001\u0000\u0000"+
		"\u0000\u041c\u0019\u0001\u0000\u0000\u0000\u041d\u041b\u0001\u0000\u0000"+
		"\u0000\u041e\u041f\u0003\u00b6[\u0000\u041f\u0420\u0005\u010c\u0000\u0000"+
		"\u0420\u0421\u0003\u001c\u000e\u0000\u0421\u001b\u0001\u0000\u0000\u0000"+
		"\u0422\u0425\u0005E\u0000\u0000\u0423\u0425\u0003`0\u0000\u0424\u0422"+
		"\u0001\u0000\u0000\u0000\u0424\u0423\u0001\u0000\u0000\u0000\u0425\u001d"+
		"\u0001\u0000\u0000\u0000\u0426\u0431\u0003&\u0013\u0000\u0427\u0428\u0005"+
		"\u00ad\u0000\u0000\u0428\u0429\u0005%\u0000\u0000\u0429\u042e\u0003*\u0015"+
		"\u0000\u042a\u042b\u0005\u0004\u0000\u0000\u042b\u042d\u0003*\u0015\u0000"+
		"\u042c\u042a\u0001\u0000\u0000\u0000\u042d\u0430\u0001\u0000\u0000\u0000"+
		"\u042e\u042c\u0001\u0000\u0000\u0000\u042e\u042f\u0001\u0000\u0000\u0000"+
		"\u042f\u0432\u0001\u0000\u0000\u0000\u0430\u042e\u0001\u0000\u0000\u0000"+
		"\u0431\u0427\u0001\u0000\u0000\u0000\u0431\u0432\u0001\u0000\u0000\u0000"+
		"\u0432\u045a\u0001\u0000\u0000\u0000\u0433\u0434\u0005\u00a4\u0000\u0000"+
		"\u0434\u0436\u0003$\u0012\u0000\u0435\u0437\u0007\u0007\u0000\u0000\u0436"+
		"\u0435\u0001\u0000\u0000\u0000\u0436\u0437\u0001\u0000\u0000\u0000\u0437"+
		"\u0439\u0001\u0000\u0000\u0000\u0438\u0433\u0001\u0000\u0000\u0000\u0438"+
		"\u0439\u0001\u0000\u0000\u0000\u0439\u044a\u0001\u0000\u0000\u0000\u043a"+
		"\u043b\u0005\u0087\u0000\u0000\u043b\u043d\u0003\"\u0011\u0000\u043c\u043e"+
		"\u0003 \u0010\u0000\u043d\u043c\u0001\u0000\u0000\u0000\u043d\u043e\u0001"+
		"\u0000\u0000\u0000\u043e\u044b\u0001\u0000\u0000\u0000\u043f\u0440\u0005"+
		"]\u0000\u0000\u0440\u0442\u0007\b\u0000\u0000\u0441\u0443\u0003$\u0012"+
		"\u0000\u0442\u0441\u0001\u0000\u0000\u0000\u0442\u0443\u0001\u0000\u0000"+
		"\u0000\u0443\u0444\u0001\u0000\u0000\u0000\u0444\u0448\u0007\u0007\u0000"+
		"\u0000\u0445\u0449\u0005\u00a9\u0000\u0000\u0446\u0447\u0005\u0105\u0000"+
		"\u0000\u0447\u0449\u0005\u00ea\u0000\u0000\u0448\u0445\u0001\u0000\u0000"+
		"\u0000\u0448\u0446\u0001\u0000\u0000\u0000\u0449\u044b\u0001\u0000\u0000"+
		"\u0000\u044a\u043a\u0001\u0000\u0000\u0000\u044a\u043f\u0001\u0000\u0000"+
		"\u0000\u044a\u044b\u0001\u0000\u0000\u0000\u044b\u045b\u0001\u0000\u0000"+
		"\u0000\u044c\u044d\u0005\u0087\u0000\u0000\u044d\u044f\u0003\"\u0011\u0000"+
		"\u044e\u0450\u0003 \u0010\u0000\u044f\u044e\u0001\u0000\u0000\u0000\u044f"+
		"\u0450\u0001\u0000\u0000\u0000\u0450\u0452\u0001\u0000\u0000\u0000\u0451"+
		"\u044c\u0001\u0000\u0000\u0000\u0451\u0452\u0001\u0000\u0000\u0000\u0452"+
		"\u0458\u0001\u0000\u0000\u0000\u0453\u0454\u0005\u00a4\u0000\u0000\u0454"+
		"\u0456\u0003$\u0012\u0000\u0455\u0457\u0007\u0007\u0000\u0000\u0456\u0455"+
		"\u0001\u0000\u0000\u0000\u0456\u0457\u0001\u0000\u0000\u0000\u0457\u0459"+
		"\u0001\u0000\u0000\u0000\u0458\u0453\u0001\u0000\u0000\u0000\u0458\u0459"+
		"\u0001\u0000\u0000\u0000\u0459\u045b\u0001\u0000\u0000\u0000\u045a\u0438"+
		"\u0001\u0000\u0000\u0000\u045a\u0451\u0001\u0000\u0000\u0000\u045b\u001f"+
		"\u0001\u0000\u0000\u0000\u045c\u045f\u0005\u0128\u0000\u0000\u045d\u045e"+
		"\u0005\u0120\u0000\u0000\u045e\u0460\u0005\u0001\u0000\u0000\u045f\u045d"+
		"\u0001\u0000\u0000\u0000\u045f\u0460\u0001\u0000\u0000\u0000\u0460\u0461"+
		"\u0001\u0000\u0000\u0000\u0461\u0462\u0003\u00b6[\u0000\u0462!\u0001\u0000"+
		"\u0000\u0000\u0463\u0467\u0005\u0019\u0000\u0000\u0464\u0467\u0003$\u0012"+
		"\u0000\u0465\u0467\u0003p8\u0000\u0466\u0463\u0001\u0000\u0000\u0000\u0466"+
		"\u0464\u0001\u0000\u0000\u0000\u0466\u0465\u0001\u0000\u0000\u0000\u0467"+
		"#\u0001\u0000\u0000\u0000\u0468\u0469\u0007\t\u0000\u0000\u0469%\u0001"+
		"\u0000\u0000\u0000\u046a\u046b\u0006\u0013\uffff\uffff\u0000\u046b\u046c"+
		"\u0003(\u0014\u0000\u046c\u047b\u0001\u0000\u0000\u0000\u046d\u046e\n"+
		"\u0002\u0000\u0000\u046e\u0470\u0005y\u0000\u0000\u046f\u0471\u0003:\u001d"+
		"\u0000\u0470\u046f\u0001\u0000\u0000\u0000\u0470\u0471\u0001\u0000\u0000"+
		"\u0000\u0471\u0472\u0001\u0000\u0000\u0000\u0472\u047a\u0003&\u0013\u0003"+
		"\u0473\u0474\n\u0001\u0000\u0000\u0474\u0476\u0007\n\u0000\u0000\u0475"+
		"\u0477\u0003:\u001d\u0000\u0476\u0475\u0001\u0000\u0000\u0000\u0476\u0477"+
		"\u0001\u0000\u0000\u0000\u0477\u0478\u0001\u0000\u0000\u0000\u0478\u047a"+
		"\u0003&\u0013\u0002\u0479\u046d\u0001\u0000\u0000\u0000\u0479\u0473\u0001"+
		"\u0000\u0000\u0000\u047a\u047d\u0001\u0000\u0000\u0000\u047b\u0479\u0001"+
		"\u0000\u0000\u0000\u047b\u047c\u0001\u0000\u0000\u0000\u047c\'\u0001\u0000"+
		"\u0000\u0000\u047d\u047b\u0001\u0000\u0000\u0000\u047e\u048f\u0003,\u0016"+
		"\u0000\u047f\u0480\u0005\u00e5\u0000\u0000\u0480\u048f\u0003\u00aaU\u0000"+
		"\u0481\u0482\u0005\u00fe\u0000\u0000\u0482\u0487\u0003`0\u0000\u0483\u0484"+
		"\u0005\u0004\u0000\u0000\u0484\u0486\u0003`0\u0000\u0485\u0483\u0001\u0000"+
		"\u0000\u0000\u0486\u0489\u0001\u0000\u0000\u0000\u0487\u0485\u0001\u0000"+
		"\u0000\u0000\u0487\u0488\u0001\u0000\u0000\u0000\u0488\u048f\u0001\u0000"+
		"\u0000\u0000\u0489\u0487\u0001\u0000\u0000\u0000\u048a\u048b\u0005\u0002"+
		"\u0000\u0000\u048b\u048c\u0003\u001e\u000f\u0000\u048c\u048d\u0005\u0003"+
		"\u0000\u0000\u048d\u048f\u0001\u0000\u0000\u0000\u048e\u047e\u0001\u0000"+
		"\u0000\u0000\u048e\u047f\u0001\u0000\u0000\u0000\u048e\u0481\u0001\u0000"+
		"\u0000\u0000\u048e\u048a\u0001\u0000\u0000\u0000\u048f)\u0001\u0000\u0000"+
		"\u0000\u0490\u0492\u0003`0\u0000\u0491\u0493\u0007\u000b\u0000\u0000\u0492"+
		"\u0491\u0001\u0000\u0000\u0000\u0492\u0493\u0001\u0000\u0000\u0000\u0493"+
		"\u0496\u0001\u0000\u0000\u0000\u0494\u0495\u0005\u00a3\u0000\u0000\u0495"+
		"\u0497\u0007\f\u0000\u0000\u0496\u0494\u0001\u0000\u0000\u0000\u0496\u0497"+
		"\u0001\u0000\u0000\u0000\u0497+\u0001\u0000\u0000\u0000\u0498\u049a\u0005"+
		"\u00d8\u0000\u0000\u0499\u049b\u0003:\u001d\u0000\u049a\u0499\u0001\u0000"+
		"\u0000\u0000\u049a\u049b\u0001\u0000\u0000\u0000\u049b\u049c\u0001\u0000"+
		"\u0000\u0000\u049c\u04a1\u0003<\u001e\u0000\u049d\u049e\u0005\u0004\u0000"+
		"\u0000\u049e\u04a0\u0003<\u001e\u0000\u049f\u049d\u0001\u0000\u0000\u0000"+
		"\u04a0\u04a3\u0001\u0000\u0000\u0000\u04a1\u049f\u0001\u0000\u0000\u0000"+
		"\u04a1\u04a2\u0001\u0000\u0000\u0000\u04a2\u04ad\u0001\u0000\u0000\u0000"+
		"\u04a3\u04a1\u0001\u0000\u0000\u0000\u04a4\u04a5\u0005d\u0000\u0000\u04a5"+
		"\u04aa\u0003>\u001f\u0000\u04a6\u04a7\u0005\u0004\u0000\u0000\u04a7\u04a9"+
		"\u0003>\u001f\u0000\u04a8\u04a6\u0001\u0000\u0000\u0000\u04a9\u04ac\u0001"+
		"\u0000\u0000\u0000\u04aa\u04a8\u0001\u0000\u0000\u0000\u04aa\u04ab\u0001"+
		"\u0000\u0000\u0000\u04ab\u04ae\u0001\u0000\u0000\u0000\u04ac\u04aa\u0001"+
		"\u0000\u0000\u0000\u04ad\u04a4\u0001\u0000\u0000\u0000\u04ad\u04ae\u0001"+
		"\u0000\u0000\u0000\u04ae\u04b1\u0001\u0000\u0000\u0000\u04af\u04b0\u0005"+
		"\u0103\u0000\u0000\u04b0\u04b2\u0003b1\u0000\u04b1\u04af\u0001\u0000\u0000"+
		"\u0000\u04b1\u04b2\u0001\u0000\u0000\u0000\u04b2\u04b6\u0001\u0000\u0000"+
		"\u0000\u04b3\u04b4\u0005k\u0000\u0000\u04b4\u04b5\u0005%\u0000\u0000\u04b5"+
		"\u04b7\u0003.\u0017\u0000\u04b6\u04b3\u0001\u0000\u0000\u0000\u04b6\u04b7"+
		"\u0001\u0000\u0000\u0000\u04b7\u04ba\u0001\u0000\u0000\u0000\u04b8\u04b9"+
		"\u0005n\u0000\u0000\u04b9\u04bb\u0003b1\u0000\u04ba\u04b8\u0001\u0000"+
		"\u0000\u0000\u04ba\u04bb\u0001\u0000\u0000\u0000\u04bb\u04c5\u0001\u0000"+
		"\u0000\u0000\u04bc\u04bd\u0005\u0104\u0000\u0000\u04bd\u04c2\u00034\u001a"+
		"\u0000\u04be\u04bf\u0005\u0004\u0000\u0000\u04bf\u04c1\u00034\u001a\u0000"+
		"\u04c0\u04be\u0001\u0000\u0000\u0000\u04c1\u04c4\u0001\u0000\u0000\u0000"+
		"\u04c2\u04c0\u0001\u0000\u0000\u0000\u04c2\u04c3\u0001\u0000\u0000\u0000"+
		"\u04c3\u04c6\u0001\u0000\u0000\u0000\u04c4\u04c2\u0001\u0000\u0000\u0000"+
		"\u04c5\u04bc\u0001\u0000\u0000\u0000\u04c5\u04c6\u0001\u0000\u0000\u0000"+
		"\u04c6-\u0001\u0000\u0000\u0000\u04c7\u04c9\u0003:\u001d\u0000\u04c8\u04c7"+
		"\u0001\u0000\u0000\u0000\u04c8\u04c9\u0001\u0000\u0000\u0000\u04c9\u04ca"+
		"\u0001\u0000\u0000\u0000\u04ca\u04cf\u00030\u0018\u0000\u04cb\u04cc\u0005"+
		"\u0004\u0000\u0000\u04cc\u04ce\u00030\u0018\u0000\u04cd\u04cb\u0001\u0000"+
		"\u0000\u0000\u04ce\u04d1\u0001\u0000\u0000\u0000\u04cf\u04cd\u0001\u0000"+
		"\u0000\u0000\u04cf\u04d0\u0001\u0000\u0000\u0000\u04d0/\u0001\u0000\u0000"+
		"\u0000\u04d1\u04cf\u0001\u0000\u0000\u0000\u04d2\u04fb\u00032\u0019\u0000"+
		"\u04d3\u04d4\u0005\u00cf\u0000\u0000\u04d4\u04dd\u0005\u0002\u0000\u0000"+
		"\u04d5\u04da\u0003`0\u0000\u04d6\u04d7\u0005\u0004\u0000\u0000\u04d7\u04d9"+
		"\u0003`0\u0000\u04d8\u04d6\u0001\u0000\u0000\u0000\u04d9\u04dc\u0001\u0000"+
		"\u0000\u0000\u04da\u04d8\u0001\u0000\u0000\u0000\u04da\u04db\u0001\u0000"+
		"\u0000\u0000\u04db\u04de\u0001\u0000\u0000\u0000\u04dc\u04da\u0001\u0000"+
		"\u0000\u0000\u04dd\u04d5\u0001\u0000\u0000\u0000\u04dd\u04de\u0001\u0000"+
		"\u0000\u0000\u04de\u04df\u0001\u0000\u0000\u0000\u04df\u04fb\u0005\u0003"+
		"\u0000\u0000\u04e0\u04e1\u00055\u0000\u0000\u04e1\u04ea\u0005\u0002\u0000"+
		"\u0000\u04e2\u04e7\u0003`0\u0000\u04e3\u04e4\u0005\u0004\u0000\u0000\u04e4"+
		"\u04e6\u0003`0\u0000\u04e5\u04e3\u0001\u0000\u0000\u0000\u04e6\u04e9\u0001"+
		"\u0000\u0000\u0000\u04e7\u04e5\u0001\u0000\u0000\u0000\u04e7\u04e8\u0001"+
		"\u0000\u0000\u0000\u04e8\u04eb\u0001\u0000\u0000\u0000\u04e9\u04e7\u0001"+
		"\u0000\u0000\u0000\u04ea\u04e2\u0001\u0000\u0000\u0000\u04ea\u04eb\u0001"+
		"\u0000\u0000\u0000\u04eb\u04ec\u0001\u0000\u0000\u0000\u04ec\u04fb\u0005"+
		"\u0003\u0000\u0000\u04ed\u04ee\u0005l\u0000\u0000\u04ee\u04ef\u0005\u00dd"+
		"\u0000\u0000\u04ef\u04f0\u0005\u0002\u0000\u0000\u04f0\u04f5\u00032\u0019"+
		"\u0000\u04f1\u04f2\u0005\u0004\u0000\u0000\u04f2\u04f4\u00032\u0019\u0000"+
		"\u04f3\u04f1\u0001\u0000\u0000\u0000\u04f4\u04f7\u0001\u0000\u0000\u0000"+
		"\u04f5\u04f3\u0001\u0000\u0000\u0000\u04f5\u04f6\u0001\u0000\u0000\u0000"+
		"\u04f6\u04f8\u0001\u0000\u0000\u0000\u04f7\u04f5\u0001\u0000\u0000\u0000"+
		"\u04f8\u04f9\u0005\u0003\u0000\u0000\u04f9\u04fb\u0001\u0000\u0000\u0000"+
		"\u04fa\u04d2\u0001\u0000\u0000\u0000\u04fa\u04d3\u0001\u0000\u0000\u0000"+
		"\u04fa\u04e0\u0001\u0000\u0000\u0000\u04fa\u04ed\u0001\u0000\u0000\u0000"+
		"\u04fb1\u0001\u0000\u0000\u0000\u04fc\u0505\u0005\u0002\u0000\u0000\u04fd"+
		"\u0502\u0003`0\u0000\u04fe\u04ff\u0005\u0004\u0000\u0000\u04ff\u0501\u0003"+
		"`0\u0000\u0500\u04fe\u0001\u0000\u0000\u0000\u0501\u0504\u0001\u0000\u0000"+
		"\u0000\u0502\u0500\u0001\u0000\u0000\u0000\u0502\u0503\u0001\u0000\u0000"+
		"\u0000\u0503\u0506\u0001\u0000\u0000\u0000\u0504\u0502\u0001\u0000\u0000"+
		"\u0000\u0505\u04fd\u0001\u0000\u0000\u0000\u0505\u0506\u0001\u0000\u0000"+
		"\u0000\u0506\u0507\u0001\u0000\u0000\u0000\u0507\u050a\u0005\u0003\u0000"+
		"\u0000\u0508\u050a\u0003`0\u0000\u0509\u04fc\u0001\u0000\u0000\u0000\u0509"+
		"\u0508\u0001\u0000\u0000\u0000\u050a3\u0001\u0000\u0000\u0000\u050b\u050c"+
		"\u0003\u00b6[\u0000\u050c\u050d\u0005\u001f\u0000\u0000\u050d\u050e\u0005"+
		"\u0002\u0000\u0000\u050e\u050f\u00036\u001b\u0000\u050f\u0510\u0005\u0003"+
		"\u0000\u0000\u05105\u0001\u0000\u0000\u0000\u0511\u0513\u0003\u00b6[\u0000"+
		"\u0512\u0511\u0001\u0000\u0000\u0000\u0512\u0513\u0001\u0000\u0000\u0000"+
		"\u0513\u051e\u0001\u0000\u0000\u0000\u0514\u0515\u0005\u00b3\u0000\u0000"+
		"\u0515\u0516\u0005%\u0000\u0000\u0516\u051b\u0003`0\u0000\u0517\u0518"+
		"\u0005\u0004\u0000\u0000\u0518\u051a\u0003`0\u0000\u0519\u0517\u0001\u0000"+
		"\u0000\u0000\u051a\u051d\u0001\u0000\u0000\u0000\u051b\u0519\u0001\u0000"+
		"\u0000\u0000\u051b\u051c\u0001\u0000\u0000\u0000\u051c\u051f\u0001\u0000"+
		"\u0000\u0000\u051d\u051b\u0001\u0000\u0000\u0000\u051e\u0514\u0001\u0000"+
		"\u0000\u0000\u051e\u051f\u0001\u0000\u0000\u0000\u051f\u052a\u0001\u0000"+
		"\u0000\u0000\u0520\u0521\u0005\u00ad\u0000\u0000\u0521\u0522\u0005%\u0000"+
		"\u0000\u0522\u0527\u0003*\u0015\u0000\u0523\u0524\u0005\u0004\u0000\u0000"+
		"\u0524\u0526\u0003*\u0015\u0000\u0525\u0523\u0001\u0000\u0000\u0000\u0526"+
		"\u0529\u0001\u0000\u0000\u0000\u0527\u0525\u0001\u0000\u0000\u0000\u0527"+
		"\u0528\u0001\u0000\u0000\u0000\u0528\u052b\u0001\u0000\u0000\u0000\u0529"+
		"\u0527\u0001\u0000\u0000\u0000\u052a\u0520\u0001\u0000\u0000\u0000\u052a"+
		"\u052b\u0001\u0000\u0000\u0000\u052b\u052d\u0001\u0000\u0000\u0000\u052c"+
		"\u052e\u0003\u008eG\u0000\u052d\u052c\u0001\u0000\u0000\u0000\u052d\u052e"+
		"\u0001\u0000\u0000\u0000\u052e7\u0001\u0000\u0000\u0000\u052f\u0531\u0003"+
		"\u00b6[\u0000\u0530\u0532\u0003\\.\u0000\u0531\u0530\u0001\u0000\u0000"+
		"\u0000\u0531\u0532\u0001\u0000\u0000\u0000\u0532\u0533\u0001\u0000\u0000"+
		"\u0000\u0533\u0534\u0005\u001f\u0000\u0000\u0534\u0535\u0005\u0002\u0000"+
		"\u0000\u0535\u0536\u0003\f\u0006\u0000\u0536\u0537\u0005\u0003\u0000\u0000"+
		"\u05379\u0001\u0000\u0000\u0000\u0538\u0539\u0007\r\u0000\u0000\u0539"+
		";\u0001\u0000\u0000\u0000\u053a\u053f\u0003`0\u0000\u053b\u053d\u0005"+
		"\u001f\u0000\u0000\u053c\u053b\u0001\u0000\u0000\u0000\u053c\u053d\u0001"+
		"\u0000\u0000\u0000\u053d\u053e\u0001\u0000\u0000\u0000\u053e\u0540\u0003"+
		"\u00b6[\u0000\u053f\u053c\u0001\u0000\u0000\u0000\u053f\u0540\u0001\u0000"+
		"\u0000\u0000\u0540\u054a\u0001\u0000\u0000\u0000\u0541\u0542\u0003j5\u0000"+
		"\u0542\u0543\u0005\u0001\u0000\u0000\u0543\u0546\u0005\u0114\u0000\u0000"+
		"\u0544\u0545\u0005\u001f\u0000\u0000\u0545\u0547\u0003\\.\u0000\u0546"+
		"\u0544\u0001\u0000\u0000\u0000\u0546\u0547\u0001\u0000\u0000\u0000\u0547"+
		"\u054a\u0001\u0000\u0000\u0000\u0548\u054a\u0005\u0114\u0000\u0000\u0549"+
		"\u053a\u0001\u0000\u0000\u0000\u0549\u0541\u0001\u0000\u0000\u0000\u0549"+
		"\u0548\u0001\u0000\u0000\u0000\u054a=\u0001\u0000\u0000\u0000\u054b\u054c"+
		"\u0006\u001f\uffff\uffff\u0000\u054c\u054d\u0003D\"\u0000\u054d\u0560"+
		"\u0001\u0000\u0000\u0000\u054e\u055c\n\u0002\u0000\u0000\u054f\u0550\u0005"+
		"4\u0000\u0000\u0550\u0551\u0005\u0080\u0000\u0000\u0551\u055d\u0003D\""+
		"\u0000\u0552\u0553\u0003@ \u0000\u0553\u0554\u0005\u0080\u0000\u0000\u0554"+
		"\u0555\u0003>\u001f\u0000\u0555\u0556\u0003B!\u0000\u0556\u055d\u0001"+
		"\u0000\u0000\u0000\u0557\u0558\u0005\u0097\u0000\u0000\u0558\u0559\u0003"+
		"@ \u0000\u0559\u055a\u0005\u0080\u0000\u0000\u055a\u055b\u0003D\"\u0000"+
		"\u055b\u055d\u0001\u0000\u0000\u0000\u055c\u054f\u0001\u0000\u0000\u0000"+
		"\u055c\u0552\u0001\u0000\u0000\u0000\u055c\u0557\u0001\u0000\u0000\u0000"+
		"\u055d\u055f\u0001\u0000\u0000\u0000\u055e\u054e\u0001\u0000\u0000\u0000"+
		"\u055f\u0562\u0001\u0000\u0000\u0000\u0560\u055e\u0001\u0000\u0000\u0000"+
		"\u0560\u0561\u0001\u0000\u0000\u0000\u0561?\u0001\u0000\u0000\u0000\u0562"+
		"\u0560\u0001\u0000\u0000\u0000\u0563\u0565\u0005v\u0000\u0000\u0564\u0563"+
		"\u0001\u0000\u0000\u0000\u0564\u0565\u0001\u0000\u0000\u0000\u0565\u0573"+
		"\u0001\u0000\u0000\u0000\u0566\u0568\u0005\u0084\u0000\u0000\u0567\u0569"+
		"\u0005\u00af\u0000\u0000\u0568\u0567\u0001\u0000\u0000\u0000\u0568\u0569"+
		"\u0001\u0000\u0000\u0000\u0569\u0573\u0001\u0000\u0000\u0000\u056a\u056c"+
		"\u0005\u00cb\u0000\u0000\u056b\u056d\u0005\u00af\u0000\u0000\u056c\u056b"+
		"\u0001\u0000\u0000\u0000\u056c\u056d\u0001\u0000\u0000\u0000\u056d\u0573"+
		"\u0001\u0000\u0000\u0000\u056e\u0570\u0005e\u0000\u0000\u056f\u0571\u0005"+
		"\u00af\u0000\u0000\u0570\u056f\u0001\u0000\u0000\u0000\u0570\u0571\u0001"+
		"\u0000\u0000\u0000\u0571\u0573\u0001\u0000\u0000\u0000\u0572\u0564\u0001"+
		"\u0000\u0000\u0000\u0572\u0566\u0001\u0000\u0000\u0000\u0572\u056a\u0001"+
		"\u0000\u0000\u0000\u0572\u056e\u0001\u0000\u0000\u0000\u0573A\u0001\u0000"+
		"\u0000\u0000\u0574\u0575\u0005\u00a7\u0000\u0000\u0575\u0583\u0003b1\u0000"+
		"\u0576\u0577\u0005\u00fc\u0000\u0000\u0577\u0578\u0005\u0002\u0000\u0000"+
		"\u0578\u057d\u0003\u00b6[\u0000\u0579\u057a\u0005\u0004\u0000\u0000\u057a"+
		"\u057c\u0003\u00b6[\u0000\u057b\u0579\u0001\u0000\u0000\u0000\u057c\u057f"+
		"\u0001\u0000\u0000\u0000\u057d\u057b\u0001\u0000\u0000\u0000\u057d\u057e"+
		"\u0001\u0000\u0000\u0000\u057e\u0580\u0001\u0000\u0000\u0000\u057f\u057d"+
		"\u0001\u0000\u0000\u0000\u0580\u0581\u0005\u0003\u0000\u0000\u0581\u0583"+
		"\u0001\u0000\u0000\u0000\u0582\u0574\u0001\u0000\u0000\u0000\u0582\u0576"+
		"\u0001\u0000\u0000\u0000\u0583C\u0001\u0000\u0000\u0000\u0584\u058b\u0003"+
		"L&\u0000\u0585\u0586\u0005\u00e7\u0000\u0000\u0586\u0587\u0003F#\u0000"+
		"\u0587\u0588\u0005\u0002\u0000\u0000\u0588\u0589\u0003`0\u0000\u0589\u058a"+
		"\u0005\u0003\u0000\u0000\u058a\u058c\u0001\u0000\u0000\u0000\u058b\u0585"+
		"\u0001\u0000\u0000\u0000\u058b\u058c\u0001\u0000\u0000\u0000\u058cE\u0001"+
		"\u0000\u0000\u0000\u058d\u058e\u0007\u000e\u0000\u0000\u058eG\u0001\u0000"+
		"\u0000\u0000\u058f\u0596\u0005T\u0000\u0000\u0590\u0592\u0005\u00f0\u0000"+
		"\u0000\u0591\u0593\u0003p8\u0000\u0592\u0591\u0001\u0000\u0000\u0000\u0592"+
		"\u0593\u0001\u0000\u0000\u0000\u0593\u0594\u0001\u0000\u0000\u0000\u0594"+
		"\u0596\u0003J%\u0000\u0595\u058f\u0001\u0000\u0000\u0000\u0595\u0590\u0001"+
		"\u0000\u0000\u0000\u0596I\u0001\u0000\u0000\u0000\u0597\u0598\u0005\u0105"+
		"\u0000\u0000\u0598\u059c\u00052\u0000\u0000\u0599\u059a\u0005\u0107\u0000"+
		"\u0000\u059a\u059c\u00052\u0000\u0000\u059b\u0597\u0001\u0000\u0000\u0000"+
		"\u059b\u0599\u0001\u0000\u0000\u0000\u059cK\u0001\u0000\u0000\u0000\u059d"+
		"\u05f0\u0003Z-\u0000\u059e\u059f\u0005\u0091\u0000\u0000\u059f\u05aa\u0005"+
		"\u0002\u0000\u0000\u05a0\u05a1\u0005\u00b3\u0000\u0000\u05a1\u05a2\u0005"+
		"%\u0000\u0000\u05a2\u05a7\u0003`0\u0000\u05a3\u05a4\u0005\u0004\u0000"+
		"\u0000\u05a4\u05a6\u0003`0\u0000\u05a5\u05a3\u0001\u0000\u0000\u0000\u05a6"+
		"\u05a9\u0001\u0000\u0000\u0000\u05a7\u05a5\u0001\u0000\u0000\u0000\u05a7"+
		"\u05a8\u0001\u0000\u0000\u0000\u05a8\u05ab\u0001\u0000\u0000\u0000\u05a9"+
		"\u05a7\u0001\u0000\u0000\u0000\u05aa\u05a0\u0001\u0000\u0000\u0000\u05aa"+
		"\u05ab\u0001\u0000\u0000\u0000\u05ab\u05b6\u0001\u0000\u0000\u0000\u05ac"+
		"\u05ad\u0005\u00ad\u0000\u0000\u05ad\u05ae\u0005%\u0000\u0000\u05ae\u05b3"+
		"\u0003*\u0015\u0000\u05af\u05b0\u0005\u0004\u0000\u0000\u05b0\u05b2\u0003"+
		"*\u0015\u0000\u05b1\u05af\u0001\u0000\u0000\u0000\u05b2\u05b5\u0001\u0000"+
		"\u0000\u0000\u05b3\u05b1\u0001\u0000\u0000\u0000\u05b3\u05b4\u0001\u0000"+
		"\u0000\u0000\u05b4\u05b7\u0001\u0000\u0000\u0000\u05b5\u05b3\u0001\u0000"+
		"\u0000\u0000\u05b6\u05ac\u0001\u0000\u0000\u0000\u05b6\u05b7\u0001\u0000"+
		"\u0000\u0000\u05b7\u05c1\u0001\u0000\u0000\u0000\u05b8\u05b9\u0005\u0093"+
		"\u0000\u0000\u05b9\u05be\u0003N\'\u0000\u05ba\u05bb\u0005\u0004\u0000"+
		"\u0000\u05bb\u05bd\u0003N\'\u0000\u05bc\u05ba\u0001\u0000\u0000\u0000"+
		"\u05bd\u05c0\u0001\u0000\u0000\u0000\u05be\u05bc\u0001\u0000\u0000\u0000"+
		"\u05be\u05bf\u0001\u0000\u0000\u0000\u05bf\u05c2\u0001\u0000\u0000\u0000"+
		"\u05c0\u05be\u0001\u0000\u0000\u0000\u05c1\u05b8\u0001\u0000\u0000\u0000"+
		"\u05c1\u05c2\u0001\u0000\u0000\u0000\u05c2\u05c4\u0001\u0000\u0000\u0000"+
		"\u05c3\u05c5\u0003P(\u0000\u05c4\u05c3\u0001\u0000\u0000\u0000\u05c4\u05c5"+
		"\u0001\u0000\u0000\u0000\u05c5\u05c9\u0001\u0000\u0000\u0000\u05c6\u05c7"+
		"\u0005\u0018\u0000\u0000\u05c7\u05c8\u0005\u008e\u0000\u0000\u05c8\u05ca"+
		"\u0003T*\u0000\u05c9\u05c6\u0001\u0000\u0000\u0000\u05c9\u05ca\u0001\u0000"+
		"\u0000\u0000\u05ca\u05cc\u0001\u0000\u0000\u0000\u05cb\u05cd\u0007\u000f"+
		"\u0000\u0000\u05cc\u05cb\u0001\u0000\u0000\u0000\u05cc\u05cd\u0001\u0000"+
		"\u0000\u0000\u05cd\u05ce\u0001\u0000\u0000\u0000\u05ce\u05cf\u0005\u00b7"+
		"\u0000\u0000\u05cf\u05d0\u0005\u0002\u0000\u0000\u05d0\u05d1\u0003\u0094"+
		"J\u0000\u05d1\u05db\u0005\u0003\u0000\u0000\u05d2\u05d3\u0005\u00e2\u0000"+
		"\u0000\u05d3\u05d8\u0003V+\u0000\u05d4\u05d5\u0005\u0004\u0000\u0000\u05d5"+
		"\u05d7\u0003V+\u0000\u05d6\u05d4\u0001\u0000\u0000\u0000\u05d7\u05da\u0001"+
		"\u0000\u0000\u0000\u05d8\u05d6\u0001\u0000\u0000\u0000\u05d8\u05d9\u0001"+
		"\u0000\u0000\u0000\u05d9\u05dc\u0001\u0000\u0000\u0000\u05da\u05d8\u0001"+
		"\u0000\u0000\u0000\u05db\u05d2\u0001\u0000\u0000\u0000\u05db\u05dc\u0001"+
		"\u0000\u0000\u0000\u05dc\u05dd\u0001\u0000\u0000\u0000\u05dd\u05de\u0005"+
		"K\u0000\u0000\u05de\u05e3\u0003X,\u0000\u05df\u05e0\u0005\u0004\u0000"+
		"\u0000\u05e0\u05e2\u0003X,\u0000\u05e1\u05df\u0001\u0000\u0000\u0000\u05e2"+
		"\u05e5\u0001\u0000\u0000\u0000\u05e3\u05e1\u0001\u0000\u0000\u0000\u05e3"+
		"\u05e4\u0001\u0000\u0000\u0000\u05e4\u05e6\u0001\u0000\u0000\u0000\u05e5"+
		"\u05e3\u0001\u0000\u0000\u0000\u05e6\u05ee\u0005\u0003\u0000\u0000\u05e7"+
		"\u05e9\u0005\u001f\u0000\u0000\u05e8\u05e7\u0001\u0000\u0000\u0000\u05e8"+
		"\u05e9\u0001\u0000\u0000\u0000\u05e9\u05ea\u0001\u0000\u0000\u0000\u05ea"+
		"\u05ec\u0003\u00b6[\u0000\u05eb\u05ed\u0003\\.\u0000\u05ec\u05eb\u0001"+
		"\u0000\u0000\u0000\u05ec\u05ed\u0001\u0000\u0000\u0000\u05ed\u05ef\u0001"+
		"\u0000\u0000\u0000\u05ee\u05e8\u0001\u0000\u0000\u0000\u05ee\u05ef\u0001"+
		"\u0000\u0000\u0000\u05ef\u05f1\u0001\u0000\u0000\u0000\u05f0\u059e\u0001"+
		"\u0000\u0000\u0000\u05f0\u05f1\u0001\u0000\u0000\u0000\u05f1M\u0001\u0000"+
		"\u0000\u0000\u05f2\u05f3\u0003`0\u0000\u05f3\u05f4\u0005\u001f\u0000\u0000"+
		"\u05f4\u05f5\u0003\u00b6[\u0000\u05f5O\u0001\u0000\u0000\u0000\u05f6\u05f7"+
		"\u0005\u00a8\u0000\u0000\u05f7\u05f8\u0005\u00d0\u0000\u0000\u05f8\u05f9"+
		"\u0005\u00b8\u0000\u0000\u05f9\u0602\u0005\u008e\u0000\u0000\u05fa\u05fb"+
		"\u0005\u0019\u0000\u0000\u05fb\u05fc\u0005\u00d1\u0000\u0000\u05fc\u05fd"+
		"\u0005\u00b8\u0000\u0000\u05fd\u05ff\u0005\u008e\u0000\u0000\u05fe\u0600"+
		"\u0003R)\u0000\u05ff\u05fe\u0001\u0000\u0000\u0000\u05ff\u0600\u0001\u0000"+
		"\u0000\u0000\u0600\u0602\u0001\u0000\u0000\u0000\u0601\u05f6\u0001\u0000"+
		"\u0000\u0000\u0601\u05fa\u0001\u0000\u0000\u0000\u0602Q\u0001\u0000\u0000"+
		"\u0000\u0603\u0604\u0005\u00de\u0000\u0000\u0604\u0605\u0005Q\u0000\u0000"+
		"\u0605\u060d\u0005\u0090\u0000\u0000\u0606\u0607\u0005\u00a5\u0000\u0000"+
		"\u0607\u0608\u0005Q\u0000\u0000\u0608\u060d\u0005\u0090\u0000\u0000\u0609"+
		"\u060a\u0005\u0105\u0000\u0000\u060a\u060b\u0005\u00f7\u0000\u0000\u060b"+
		"\u060d\u0005\u00d1\u0000\u0000\u060c\u0603\u0001\u0000\u0000\u0000\u060c"+
		"\u0606\u0001\u0000\u0000\u0000\u060c\u0609\u0001\u0000\u0000\u0000\u060d"+
		"S\u0001\u0000\u0000\u0000\u060e\u060f\u0005\n\u0000\u0000\u060f\u0610"+
		"\u0005\u00ed\u0000\u0000\u0610\u0611\u0005\u0098\u0000\u0000\u0611\u0622"+
		"\u0005\u00d0\u0000\u0000\u0612\u0613\u0005\n\u0000\u0000\u0613\u0614\u0005"+
		"\u00b5\u0000\u0000\u0614\u0615\u0005\u0082\u0000\u0000\u0615\u0622\u0005"+
		"\u00d0\u0000\u0000\u0616\u0617\u0005\n\u0000\u0000\u0617\u0618\u0005\u00ed"+
		"\u0000\u0000\u0618\u0619\u0005`\u0000\u0000\u0619\u0622\u0003\u00b6[\u0000"+
		"\u061a\u061b\u0005\n\u0000\u0000\u061b\u061c\u0005\u00ed\u0000\u0000\u061c"+
		"\u061d\u0005\u0082\u0000\u0000\u061d\u0622\u0003\u00b6[\u0000\u061e\u061f"+
		"\u0005\n\u0000\u0000\u061f\u0620\u0005\u00ed\u0000\u0000\u0620\u0622\u0003"+
		"\u00b6[\u0000\u0621\u060e\u0001\u0000\u0000\u0000\u0621\u0612\u0001\u0000"+
		"\u0000\u0000\u0621\u0616\u0001\u0000\u0000\u0000\u0621\u061a\u0001\u0000"+
		"\u0000\u0000\u0621\u061e\u0001\u0000\u0000\u0000\u0622U\u0001\u0000\u0000"+
		"\u0000\u0623\u0624\u0003\u00b6[\u0000\u0624\u0625\u0005\u010c\u0000\u0000"+
		"\u0625\u0626\u0005\u0002\u0000\u0000\u0626\u062b\u0003\u00b6[\u0000\u0627"+
		"\u0628\u0005\u0004\u0000\u0000\u0628\u062a\u0003\u00b6[\u0000\u0629\u0627"+
		"\u0001\u0000\u0000\u0000\u062a\u062d\u0001\u0000\u0000\u0000\u062b\u0629"+
		"\u0001\u0000\u0000\u0000\u062b\u062c\u0001\u0000\u0000\u0000\u062c\u062e"+
		"\u0001\u0000\u0000\u0000\u062d\u062b\u0001\u0000\u0000\u0000\u062e\u062f"+
		"\u0005\u0003\u0000\u0000\u062fW\u0001\u0000\u0000\u0000\u0630\u0631\u0003"+
		"\u00b6[\u0000\u0631\u0632\u0005\u001f\u0000\u0000\u0632\u0633\u0003`0"+
		"\u0000\u0633Y\u0001\u0000\u0000\u0000\u0634\u063c\u0003^/\u0000\u0635"+
		"\u0637\u0005\u001f\u0000\u0000\u0636\u0635\u0001\u0000\u0000\u0000\u0636"+
		"\u0637\u0001\u0000\u0000\u0000\u0637\u0638\u0001\u0000\u0000\u0000\u0638"+
		"\u063a\u0003\u00b6[\u0000\u0639\u063b\u0003\\.\u0000\u063a\u0639\u0001"+
		"\u0000\u0000\u0000\u063a\u063b\u0001\u0000\u0000\u0000\u063b\u063d\u0001"+
		"\u0000\u0000\u0000\u063c\u0636\u0001\u0000\u0000\u0000\u063c\u063d\u0001"+
		"\u0000\u0000\u0000\u063d[\u0001\u0000\u0000\u0000\u063e\u063f\u0005\u0002"+
		"\u0000\u0000\u063f\u0644\u0003\u00b6[\u0000\u0640\u0641\u0005\u0004\u0000"+
		"\u0000\u0641\u0643\u0003\u00b6[\u0000\u0642\u0640\u0001\u0000\u0000\u0000"+
		"\u0643\u0646\u0001\u0000\u0000\u0000\u0644\u0642\u0001\u0000\u0000\u0000"+
		"\u0644\u0645\u0001\u0000\u0000\u0000\u0645\u0647\u0001\u0000\u0000\u0000"+
		"\u0646\u0644\u0001\u0000\u0000\u0000\u0647\u0648\u0005\u0003\u0000\u0000"+
		"\u0648]\u0001\u0000\u0000\u0000\u0649\u064b\u0003\u00aaU\u0000\u064a\u064c"+
		"\u0003\u00acV\u0000\u064b\u064a\u0001\u0000\u0000\u0000\u064b\u064c\u0001"+
		"\u0000\u0000\u0000\u064c\u067f\u0001\u0000\u0000\u0000\u064d\u064e\u0005"+
		"\u0002\u0000\u0000\u064e\u064f\u0003\f\u0006\u0000\u064f\u0650\u0005\u0003"+
		"\u0000\u0000\u0650\u067f\u0001\u0000\u0000\u0000\u0651\u0652\u0005\u00f8"+
		"\u0000\u0000\u0652\u0653\u0005\u0002\u0000\u0000\u0653\u0658\u0003`0\u0000"+
		"\u0654\u0655\u0005\u0004\u0000\u0000\u0655\u0657\u0003`0\u0000\u0656\u0654"+
		"\u0001\u0000\u0000\u0000\u0657\u065a\u0001\u0000\u0000\u0000\u0658\u0656"+
		"\u0001\u0000\u0000\u0000\u0658\u0659\u0001\u0000\u0000\u0000\u0659\u065b"+
		"\u0001\u0000\u0000\u0000\u065a\u0658\u0001\u0000\u0000\u0000\u065b\u065e"+
		"\u0005\u0003\u0000\u0000\u065c\u065d\u0005\u0105\u0000\u0000\u065d\u065f"+
		"\u0005\u00ae\u0000\u0000\u065e\u065c\u0001\u0000\u0000\u0000\u065e\u065f"+
		"\u0001\u0000\u0000\u0000\u065f\u067f\u0001\u0000\u0000\u0000\u0660\u0661"+
		"\u0005\u0120\u0000\u0000\u0661\u0663\u0005\u0001\u0000\u0000\u0662\u0660"+
		"\u0001\u0000\u0000\u0000\u0662\u0663\u0001\u0000\u0000\u0000\u0663\u0664"+
		"\u0001\u0000\u0000\u0000\u0664\u0665\u0005\u00f8\u0000\u0000\u0665\u0666"+
		"\u0005\u0002\u0000\u0000\u0666\u066b\u0003`0\u0000\u0667\u0668\u0005\u0004"+
		"\u0000\u0000\u0668\u066a\u0003`0\u0000\u0669\u0667\u0001\u0000\u0000\u0000"+
		"\u066a\u066d\u0001\u0000\u0000\u0000\u066b\u0669\u0001\u0000\u0000\u0000"+
		"\u066b\u066c\u0001\u0000\u0000\u0000\u066c\u066e\u0001\u0000\u0000\u0000"+
		"\u066d\u066b\u0001\u0000\u0000\u0000\u066e\u0671\u0005\u0003\u0000\u0000"+
		"\u066f\u0670\u0005\u0105\u0000\u0000\u0670\u0672\u0005\u00ae\u0000\u0000"+
		"\u0671\u066f\u0001\u0000\u0000\u0000\u0671\u0672\u0001\u0000\u0000\u0000"+
		"\u0672\u067f\u0001\u0000\u0000\u0000\u0673\u067f\u0003f3\u0000\u0674\u067f"+
		"\u0003p8\u0000\u0675\u0676\u0005\u0083\u0000\u0000\u0676\u0677\u0005\u0002"+
		"\u0000\u0000\u0677\u0678\u0003\f\u0006\u0000\u0678\u0679\u0005\u0003\u0000"+
		"\u0000\u0679\u067f\u0001\u0000\u0000\u0000\u067a\u067b\u0005\u0002\u0000"+
		"\u0000\u067b\u067c\u0003>\u001f\u0000\u067c\u067d\u0005\u0003\u0000\u0000"+
		"\u067d\u067f\u0001\u0000\u0000\u0000\u067e\u0649\u0001\u0000\u0000\u0000"+
		"\u067e\u064d\u0001\u0000\u0000\u0000\u067e\u0651\u0001\u0000\u0000\u0000"+
		"\u067e\u0662\u0001\u0000\u0000\u0000\u067e\u0673\u0001\u0000\u0000\u0000"+
		"\u067e\u0674\u0001\u0000\u0000\u0000\u067e\u0675\u0001\u0000\u0000\u0000"+
		"\u067e\u067a\u0001\u0000\u0000\u0000\u067f_\u0001\u0000\u0000\u0000\u0680"+
		"\u0681\u0003b1\u0000\u0681a\u0001\u0000\u0000\u0000\u0682\u0683\u0006"+
		"1\uffff\uffff\u0000\u0683\u0685\u0003h4\u0000\u0684\u0686\u0003d2\u0000"+
		"\u0685\u0684\u0001\u0000\u0000\u0000\u0685\u0686\u0001\u0000\u0000\u0000"+
		"\u0686\u068a\u0001\u0000\u0000\u0000\u0687\u0688\u0005\u00a0\u0000\u0000"+
		"\u0688\u068a\u0003b1\u0003\u0689\u0682\u0001\u0000\u0000\u0000\u0689\u0687"+
		"\u0001\u0000\u0000\u0000\u068a\u0693\u0001\u0000\u0000\u0000\u068b\u068c"+
		"\n\u0002\u0000\u0000\u068c\u068d\u0005\u001c\u0000\u0000\u068d\u0692\u0003"+
		"b1\u0003\u068e\u068f\n\u0001\u0000\u0000\u068f\u0690\u0005\u00ac\u0000"+
		"\u0000\u0690\u0692\u0003b1\u0002\u0691\u068b\u0001\u0000\u0000\u0000\u0691"+
		"\u068e\u0001\u0000\u0000\u0000\u0692\u0695\u0001\u0000\u0000\u0000\u0693"+
		"\u0691\u0001\u0000\u0000\u0000\u0693\u0694\u0001\u0000\u0000\u0000\u0694"+
		"c\u0001\u0000\u0000\u0000\u0695\u0693\u0001\u0000\u0000\u0000\u0696\u0697"+
		"\u0003t:\u0000\u0697\u0698\u0003v;\u0000\u0698\u0699\u0005\u0002\u0000"+
		"\u0000\u0699\u069a\u0003f3\u0000\u069a\u069b\u0005\u0003\u0000\u0000\u069b"+
		"\u06ef\u0001\u0000\u0000\u0000\u069c\u069e\u0005\u00a0\u0000\u0000\u069d"+
		"\u069c\u0001\u0000\u0000\u0000\u069d\u069e\u0001\u0000\u0000\u0000\u069e"+
		"\u06a1\u0001\u0000\u0000\u0000\u069f\u06a2\u0005\u0119\u0000\u0000\u06a0"+
		"\u06a2\u0003\u00ba]\u0000\u06a1\u069f\u0001\u0000\u0000\u0000\u06a1\u06a0"+
		"\u0001\u0000\u0000\u0000\u06a2\u06a4\u0001\u0000\u0000\u0000\u06a3\u06a5"+
		"\u0005\u0114\u0000\u0000\u06a4\u06a3\u0001\u0000\u0000\u0000\u06a4\u06a5"+
		"\u0001\u0000\u0000\u0000\u06a5\u06a6\u0001\u0000\u0000\u0000\u06a6\u06ef"+
		"\u0003h4\u0000\u06a7\u06a8\u0005\u00aa\u0000\u0000\u06a8\u06ab\u0005\u0002"+
		"\u0000\u0000\u06a9\u06aa\u0005\u0120\u0000\u0000\u06aa\u06ac\u0005\u0001"+
		"\u0000\u0000\u06ab\u06a9\u0001\u0000\u0000\u0000\u06ab\u06ac\u0001\u0000"+
		"\u0000\u0000\u06ac\u06ad\u0001\u0000\u0000\u0000\u06ad\u06ae\u0003t:\u0000"+
		"\u06ae\u06af\u0005\u0003\u0000\u0000\u06af\u06b0\u0003h4\u0000\u06b0\u06ef"+
		"\u0001\u0000\u0000\u0000\u06b1\u06b2\u0003t:\u0000\u06b2\u06b3\u0003h"+
		"4\u0000\u06b3\u06ef\u0001\u0000\u0000\u0000\u06b4\u06b5\u0003t:\u0000"+
		"\u06b5\u06b6\u0003v;\u0000\u06b6\u06b7\u0005\u0002\u0000\u0000\u06b7\u06b8"+
		"\u0003\f\u0006\u0000\u06b8\u06b9\u0005\u0003\u0000\u0000\u06b9\u06ef\u0001"+
		"\u0000\u0000\u0000\u06ba\u06bc\u0005\u00a0\u0000\u0000\u06bb\u06ba\u0001"+
		"\u0000\u0000\u0000\u06bb\u06bc\u0001\u0000\u0000\u0000\u06bc\u06bd\u0001"+
		"\u0000\u0000\u0000\u06bd\u06be\u0005$\u0000\u0000\u06be\u06bf\u0003h4"+
		"\u0000\u06bf\u06c0\u0005\u001c\u0000\u0000\u06c0\u06c1\u0003h4\u0000\u06c1"+
		"\u06ef\u0001\u0000\u0000\u0000\u06c2\u06c4\u0005\u00a0\u0000\u0000\u06c3"+
		"\u06c2\u0001\u0000\u0000\u0000\u06c3\u06c4\u0001\u0000\u0000\u0000\u06c4"+
		"\u06c5\u0001\u0000\u0000\u0000\u06c5\u06c6\u0005s\u0000\u0000\u06c6\u06c7"+
		"\u0005\u0002\u0000\u0000\u06c7\u06cc\u0003`0\u0000\u06c8\u06c9\u0005\u0004"+
		"\u0000\u0000\u06c9\u06cb\u0003`0\u0000\u06ca\u06c8\u0001\u0000\u0000\u0000"+
		"\u06cb\u06ce\u0001\u0000\u0000\u0000\u06cc\u06ca\u0001\u0000\u0000\u0000"+
		"\u06cc\u06cd\u0001\u0000\u0000\u0000\u06cd\u06cf\u0001\u0000\u0000\u0000"+
		"\u06ce\u06cc\u0001\u0000\u0000\u0000\u06cf\u06d0\u0005\u0003\u0000\u0000"+
		"\u06d0\u06ef\u0001\u0000\u0000\u0000\u06d1\u06d3\u0005\u00a0\u0000\u0000"+
		"\u06d2\u06d1\u0001\u0000\u0000\u0000\u06d2\u06d3\u0001\u0000\u0000\u0000"+
		"\u06d3\u06d4\u0001\u0000\u0000\u0000\u06d4\u06d5\u0005s\u0000\u0000\u06d5"+
		"\u06d6\u0005\u0002\u0000\u0000\u06d6\u06d7\u0003\f\u0006\u0000\u06d7\u06d8"+
		"\u0005\u0003\u0000\u0000\u06d8\u06ef\u0001\u0000\u0000\u0000\u06d9\u06db"+
		"\u0005\u00a0\u0000\u0000\u06da\u06d9\u0001\u0000\u0000\u0000\u06da\u06db"+
		"\u0001\u0000\u0000\u0000\u06db\u06dc\u0001\u0000\u0000\u0000\u06dc\u06dd"+
		"\u0005\u0086\u0000\u0000\u06dd\u06e0\u0003h4\u0000\u06de\u06df\u0005U"+
		"\u0000\u0000\u06df\u06e1\u0003h4\u0000\u06e0\u06de\u0001\u0000\u0000\u0000"+
		"\u06e0\u06e1\u0001\u0000\u0000\u0000\u06e1\u06ef\u0001\u0000\u0000\u0000"+
		"\u06e2\u06e4\u0005~\u0000\u0000\u06e3\u06e5\u0005\u00a0\u0000\u0000\u06e4"+
		"\u06e3\u0001\u0000\u0000\u0000\u06e4\u06e5\u0001\u0000\u0000\u0000\u06e5"+
		"\u06e6\u0001\u0000\u0000\u0000\u06e6\u06ef\u0005\u00a1\u0000\u0000\u06e7"+
		"\u06e9\u0005~\u0000\u0000\u06e8\u06ea\u0005\u00a0\u0000\u0000\u06e9\u06e8"+
		"\u0001\u0000\u0000\u0000\u06e9\u06ea\u0001\u0000\u0000\u0000\u06ea\u06eb"+
		"\u0001\u0000\u0000\u0000\u06eb\u06ec\u0005L\u0000\u0000\u06ec\u06ed\u0005"+
		"d\u0000\u0000\u06ed\u06ef\u0003h4\u0000\u06ee\u0696\u0001\u0000\u0000"+
		"\u0000\u06ee\u069d\u0001\u0000\u0000\u0000\u06ee\u06a7\u0001\u0000\u0000"+
		"\u0000\u06ee\u06b1\u0001\u0000\u0000\u0000\u06ee\u06b4\u0001\u0000\u0000"+
		"\u0000\u06ee\u06bb\u0001\u0000\u0000\u0000\u06ee\u06c3\u0001\u0000\u0000"+
		"\u0000\u06ee\u06d2\u0001\u0000\u0000\u0000\u06ee\u06da\u0001\u0000\u0000"+
		"\u0000\u06ee\u06e2\u0001\u0000\u0000\u0000\u06ee\u06e7\u0001\u0000\u0000"+
		"\u0000\u06efe\u0001\u0000\u0000\u0000\u06f0\u06f1\u0003\u00aaU\u0000\u06f1"+
		"\u06f2\u0005\u0002\u0000\u0000\u06f2\u06f7\u0003`0\u0000\u06f3\u06f4\u0005"+
		"\u0004\u0000\u0000\u06f4\u06f6\u0003`0\u0000\u06f5\u06f3\u0001\u0000\u0000"+
		"\u0000\u06f6\u06f9\u0001\u0000\u0000\u0000\u06f7\u06f5\u0001\u0000\u0000"+
		"\u0000\u06f7\u06f8\u0001\u0000\u0000\u0000\u06f8\u06fa\u0001\u0000\u0000"+
		"\u0000\u06f9\u06f7\u0001\u0000\u0000\u0000\u06fa\u06fb\u0005\u0003\u0000"+
		"\u0000\u06fbg\u0001\u0000\u0000\u0000\u06fc\u06fd\u00064\uffff\uffff\u0000"+
		"\u06fd\u06ff\u0003j5\u0000\u06fe\u0700\u0003\u00bc^\u0000\u06ff\u06fe"+
		"\u0001\u0000\u0000\u0000\u06ff\u0700\u0001\u0000\u0000\u0000\u0700\u0705"+
		"\u0001\u0000\u0000\u0000\u0701\u0705\u0003j5\u0000\u0702\u0703\u0007\u0010"+
		"\u0000\u0000\u0703\u0705\u0003h4\u0005\u0704\u06fc\u0001\u0000\u0000\u0000"+
		"\u0704\u0701\u0001\u0000\u0000\u0000\u0704\u0702\u0001\u0000\u0000\u0000"+
		"\u0705\u071e\u0001\u0000\u0000\u0000\u0706\u0707\n\u0004\u0000\u0000\u0707"+
		"\u0708\u0007\u0011\u0000\u0000\u0708\u071d\u0003h4\u0005\u0709\u070a\n"+
		"\u0003\u0000\u0000\u070a\u070b\u0007\u0010\u0000\u0000\u070b\u071d\u0003"+
		"h4\u0004\u070c\u070d\n\u0002\u0000\u0000\u070d\u070e\u0005\u00aa\u0000"+
		"\u0000\u070e\u0711\u0005\u0002\u0000\u0000\u070f\u0710\u0005\u0120\u0000"+
		"\u0000\u0710\u0712\u0005\u0001\u0000\u0000\u0711\u070f\u0001\u0000\u0000"+
		"\u0000\u0711\u0712\u0001\u0000\u0000\u0000\u0712\u0713\u0001\u0000\u0000"+
		"\u0000\u0713\u0714\u0007\u0012\u0000\u0000\u0714\u0715\u0005\u0003\u0000"+
		"\u0000\u0715\u071d\u0003h4\u0003\u0716\u0717\n\u0001\u0000\u0000\u0717"+
		"\u0718\u0005\u0117\u0000\u0000\u0718\u071d\u0003h4\u0002\u0719\u071a\n"+
		"\u0006\u0000\u0000\u071a\u071b\u0005!\u0000\u0000\u071b\u071d\u0003r9"+
		"\u0000\u071c\u0706\u0001\u0000\u0000\u0000\u071c\u0709\u0001\u0000\u0000"+
		"\u0000\u071c\u070c\u0001\u0000\u0000\u0000\u071c\u0716\u0001\u0000\u0000"+
		"\u0000\u071c\u0719\u0001\u0000\u0000\u0000\u071d\u0720\u0001\u0000\u0000"+
		"\u0000\u071e\u071c\u0001\u0000\u0000\u0000\u071e\u071f\u0001\u0000\u0000"+
		"\u0000\u071fi\u0001\u0000\u0000\u0000\u0720\u071e\u0001\u0000\u0000\u0000"+
		"\u0721\u0722\u00065\uffff\uffff\u0000\u0722\u086a\u0005\u00a1\u0000\u0000"+
		"\u0723\u086a\u0003z=\u0000\u0724\u0725\u0003\u00b6[\u0000\u0725\u0726"+
		"\u0003p8\u0000\u0726\u086a\u0001\u0000\u0000\u0000\u0727\u0728\u0005N"+
		"\u0000\u0000\u0728\u0729\u0005\u00bc\u0000\u0000\u0729\u086a\u0003p8\u0000"+
		"\u072a\u072b\u0003p8\u0000\u072b\u072e\u0005\u0128\u0000\u0000\u072c\u072d"+
		"\u0005\u0120\u0000\u0000\u072d\u072f\u0005\u0001\u0000\u0000\u072e\u072c"+
		"\u0001\u0000\u0000\u0000\u072e\u072f\u0001\u0000\u0000\u0000\u072f\u0730"+
		"\u0001\u0000\u0000\u0000\u0730\u0731\u0003\u00b6[\u0000\u0731\u086a\u0001"+
		"\u0000\u0000\u0000\u0732\u086a\u0003\u00b8\\\u0000\u0733\u086a\u0003x"+
		"<\u0000\u0734\u086a\u0003p8\u0000\u0735\u086a\u0005\u011c\u0000\u0000"+
		"\u0736\u086a\u0005\u0118\u0000\u0000\u0737\u0738\u0005\u00ba\u0000\u0000"+
		"\u0738\u0739\u0005\u0002\u0000\u0000\u0739\u073a\u0003h4\u0000\u073a\u073b"+
		"\u0005s\u0000\u0000\u073b\u073c\u0003h4\u0000\u073c\u073d\u0005\u0003"+
		"\u0000\u0000\u073d\u086a\u0001\u0000\u0000\u0000\u073e\u073f\u0005\u0002"+
		"\u0000\u0000\u073f\u0742\u0003`0\u0000\u0740\u0741\u0005\u0004\u0000\u0000"+
		"\u0741\u0743\u0003`0\u0000\u0742\u0740\u0001\u0000\u0000\u0000\u0743\u0744"+
		"\u0001\u0000\u0000\u0000\u0744\u0742\u0001\u0000\u0000\u0000\u0744\u0745"+
		"\u0001\u0000\u0000\u0000\u0745\u0746\u0001\u0000\u0000\u0000\u0746\u0747"+
		"\u0005\u0003\u0000\u0000\u0747\u086a\u0001\u0000\u0000\u0000\u0748\u0749"+
		"\u0005\u00d0\u0000\u0000\u0749\u074a\u0005\u0002\u0000\u0000\u074a\u074f"+
		"\u0003`0\u0000\u074b\u074c\u0005\u0004\u0000\u0000\u074c\u074e\u0003`"+
		"0\u0000\u074d\u074b\u0001\u0000\u0000\u0000\u074e\u0751\u0001\u0000\u0000"+
		"\u0000\u074f\u074d\u0001\u0000\u0000\u0000\u074f\u0750\u0001\u0000\u0000"+
		"\u0000\u0750\u0752\u0001\u0000\u0000\u0000\u0751\u074f\u0001\u0000\u0000"+
		"\u0000\u0752\u0753\u0005\u0003\u0000\u0000\u0753\u086a\u0001\u0000\u0000"+
		"\u0000\u0754\u0755\u0005\u0088\u0000\u0000\u0755\u0757\u0005\u0002\u0000"+
		"\u0000\u0756\u0758\u0003:\u001d\u0000\u0757\u0756\u0001\u0000\u0000\u0000"+
		"\u0757\u0758\u0001\u0000\u0000\u0000\u0758\u0759\u0001\u0000\u0000\u0000"+
		"\u0759\u075c\u0003`0\u0000\u075a\u075b\u0005\u0004\u0000\u0000\u075b\u075d"+
		"\u0003p8\u0000\u075c\u075a\u0001\u0000\u0000\u0000\u075c\u075d\u0001\u0000"+
		"\u0000\u0000\u075d\u0761\u0001\u0000\u0000\u0000\u075e\u075f\u0005\u00a7"+
		"\u0000\u0000\u075f\u0760\u0005\u00b2\u0000\u0000\u0760\u0762\u0003H$\u0000"+
		"\u0761\u075e\u0001\u0000\u0000\u0000\u0761\u0762\u0001\u0000\u0000\u0000"+
		"\u0762\u0763\u0001\u0000\u0000\u0000\u0763\u0764\u0005\u0003\u0000\u0000"+
		"\u0764\u0765\u0005\u0106\u0000\u0000\u0765\u0766\u0005k\u0000\u0000\u0766"+
		"\u0767\u0005\u0002\u0000\u0000\u0767\u0768\u0005\u00ad\u0000\u0000\u0768"+
		"\u0769\u0005%\u0000\u0000\u0769\u076e\u0003*\u0015\u0000\u076a\u076b\u0005"+
		"\u0004\u0000\u0000\u076b\u076d\u0003*\u0015\u0000\u076c\u076a\u0001\u0000"+
		"\u0000\u0000\u076d\u0770\u0001\u0000\u0000\u0000\u076e\u076c\u0001\u0000"+
		"\u0000\u0000\u076e\u076f\u0001\u0000\u0000\u0000\u076f\u0771\u0001\u0000"+
		"\u0000\u0000\u0770\u076e\u0001\u0000\u0000\u0000\u0771\u0772\u0005\u0003"+
		"\u0000\u0000\u0772\u086a\u0001\u0000\u0000\u0000\u0773\u0775\u0003l6\u0000"+
		"\u0774\u0773\u0001\u0000\u0000\u0000\u0774\u0775\u0001\u0000\u0000\u0000"+
		"\u0775\u0776\u0001\u0000\u0000\u0000\u0776\u0777\u0003\u00aaU\u0000\u0777"+
		"\u077b\u0005\u0002\u0000\u0000\u0778\u0779\u0003\u00b6[\u0000\u0779\u077a"+
		"\u0005\u0001\u0000\u0000\u077a\u077c\u0001\u0000\u0000\u0000\u077b\u0778"+
		"\u0001\u0000\u0000\u0000\u077b\u077c\u0001\u0000\u0000\u0000\u077c\u077d"+
		"\u0001\u0000\u0000\u0000\u077d\u077e\u0005\u0114\u0000\u0000\u077e\u0780"+
		"\u0005\u0003\u0000\u0000\u077f\u0781\u0003\u0088D\u0000\u0780\u077f\u0001"+
		"\u0000\u0000\u0000\u0780\u0781\u0001\u0000\u0000\u0000\u0781\u0783\u0001"+
		"\u0000\u0000\u0000\u0782\u0784\u0003\u008cF\u0000\u0783\u0782\u0001\u0000"+
		"\u0000\u0000\u0783\u0784\u0001\u0000\u0000\u0000\u0784\u086a\u0001\u0000"+
		"\u0000\u0000\u0785\u0787\u0003l6\u0000\u0786\u0785\u0001\u0000\u0000\u0000"+
		"\u0786\u0787\u0001\u0000\u0000\u0000\u0787\u0788\u0001\u0000\u0000\u0000"+
		"\u0788\u0789\u0003\u00aaU\u0000\u0789\u0795\u0005\u0002\u0000\u0000\u078a"+
		"\u078c\u0003:\u001d\u0000\u078b\u078a\u0001\u0000\u0000\u0000\u078b\u078c"+
		"\u0001\u0000\u0000\u0000\u078c\u078d\u0001\u0000\u0000\u0000\u078d\u0792"+
		"\u0003`0\u0000\u078e\u078f\u0005\u0004\u0000\u0000\u078f\u0791\u0003`"+
		"0\u0000\u0790\u078e\u0001\u0000\u0000\u0000\u0791\u0794\u0001\u0000\u0000"+
		"\u0000\u0792\u0790\u0001\u0000\u0000\u0000\u0792\u0793\u0001\u0000\u0000"+
		"\u0000\u0793\u0796\u0001\u0000\u0000\u0000\u0794\u0792\u0001\u0000\u0000"+
		"\u0000\u0795\u078b\u0001\u0000\u0000\u0000\u0795\u0796\u0001\u0000\u0000"+
		"\u0000\u0796\u07a1\u0001\u0000\u0000\u0000\u0797\u0798\u0005\u00ad\u0000"+
		"\u0000\u0798\u0799\u0005%\u0000\u0000\u0799\u079e\u0003*\u0015\u0000\u079a"+
		"\u079b\u0005\u0004\u0000\u0000\u079b\u079d\u0003*\u0015\u0000\u079c\u079a"+
		"\u0001\u0000\u0000\u0000\u079d\u07a0\u0001\u0000\u0000\u0000\u079e\u079c"+
		"\u0001\u0000\u0000\u0000\u079e\u079f\u0001\u0000\u0000\u0000\u079f\u07a2"+
		"\u0001\u0000\u0000\u0000\u07a0\u079e\u0001\u0000\u0000\u0000\u07a1\u0797"+
		"\u0001\u0000\u0000\u0000\u07a1\u07a2\u0001\u0000\u0000\u0000\u07a2\u07a3"+
		"\u0001\u0000\u0000\u0000\u07a3\u07a5\u0005\u0003\u0000\u0000\u07a4\u07a6"+
		"\u0003\u0088D\u0000\u07a5\u07a4\u0001\u0000\u0000\u0000\u07a5\u07a6\u0001"+
		"\u0000\u0000\u0000\u07a6\u07ab\u0001\u0000\u0000\u0000\u07a7\u07a9\u0003"+
		"n7\u0000\u07a8\u07a7\u0001\u0000\u0000\u0000\u07a8\u07a9\u0001\u0000\u0000"+
		"\u0000\u07a9\u07aa\u0001\u0000\u0000\u0000\u07aa\u07ac\u0003\u008cF\u0000"+
		"\u07ab\u07a8\u0001\u0000\u0000\u0000\u07ab\u07ac\u0001\u0000\u0000\u0000"+
		"\u07ac\u086a\u0001\u0000\u0000\u0000\u07ad\u07ae\u0003\u00b6[\u0000\u07ae"+
		"\u07af\u0003\u008cF\u0000\u07af\u086a\u0001\u0000\u0000\u0000\u07b0\u07b1"+
		"\u0003\u00b6[\u0000\u07b1\u07b2\u0005\u000b\u0000\u0000\u07b2\u07b3\u0003"+
		"`0\u0000\u07b3\u086a\u0001\u0000\u0000\u0000\u07b4\u07bd\u0005\u0002\u0000"+
		"\u0000\u07b5\u07ba\u0003\u00b6[\u0000\u07b6\u07b7\u0005\u0004\u0000\u0000"+
		"\u07b7\u07b9\u0003\u00b6[\u0000\u07b8\u07b6\u0001\u0000\u0000\u0000\u07b9"+
		"\u07bc\u0001\u0000\u0000\u0000\u07ba\u07b8\u0001\u0000\u0000\u0000\u07ba"+
		"\u07bb\u0001\u0000\u0000\u0000\u07bb\u07be\u0001\u0000\u0000\u0000\u07bc"+
		"\u07ba\u0001\u0000\u0000\u0000\u07bd\u07b5\u0001\u0000\u0000\u0000\u07bd"+
		"\u07be\u0001\u0000\u0000\u0000\u07be\u07bf\u0001\u0000\u0000\u0000\u07bf"+
		"\u07c0\u0005\u0003\u0000\u0000\u07c0\u07c1\u0005\u000b\u0000\u0000\u07c1"+
		"\u086a\u0003`0\u0000\u07c2\u07c3\u0005\u0002\u0000\u0000\u07c3\u07c4\u0003"+
		"\f\u0006\u0000\u07c4\u07c5\u0005\u0003\u0000\u0000\u07c5\u086a\u0001\u0000"+
		"\u0000\u0000\u07c6\u07c7\u0005Y\u0000\u0000\u07c7\u07c8\u0005\u0002\u0000"+
		"\u0000\u07c8\u07c9\u0003\f\u0006\u0000\u07c9\u07ca\u0005\u0003\u0000\u0000"+
		"\u07ca\u086a\u0001\u0000\u0000\u0000\u07cb\u07cc\u0005(\u0000\u0000\u07cc"+
		"\u07ce\u0003`0\u0000\u07cd\u07cf\u0003\u0086C\u0000\u07ce\u07cd\u0001"+
		"\u0000\u0000\u0000\u07cf\u07d0\u0001\u0000\u0000\u0000\u07d0\u07ce\u0001"+
		"\u0000\u0000\u0000\u07d0\u07d1\u0001\u0000\u0000\u0000\u07d1\u07d4\u0001"+
		"\u0000\u0000\u0000\u07d2\u07d3\u0005P\u0000\u0000\u07d3\u07d5\u0003`0"+
		"\u0000\u07d4\u07d2\u0001\u0000\u0000\u0000\u07d4\u07d5\u0001\u0000\u0000"+
		"\u0000\u07d5\u07d6\u0001\u0000\u0000\u0000\u07d6\u07d7\u0005R\u0000\u0000"+
		"\u07d7\u086a\u0001\u0000\u0000\u0000\u07d8\u07da\u0005(\u0000\u0000\u07d9"+
		"\u07db\u0003\u0086C\u0000\u07da\u07d9\u0001\u0000\u0000\u0000\u07db\u07dc"+
		"\u0001\u0000\u0000\u0000\u07dc\u07da\u0001\u0000\u0000\u0000\u07dc\u07dd"+
		"\u0001\u0000\u0000\u0000\u07dd\u07e0\u0001\u0000\u0000\u0000\u07de\u07df"+
		"\u0005P\u0000\u0000\u07df\u07e1\u0003`0\u0000\u07e0\u07de\u0001\u0000"+
		"\u0000\u0000\u07e0\u07e1\u0001\u0000\u0000\u0000\u07e1\u07e2\u0001\u0000"+
		"\u0000\u0000\u07e2\u07e3\u0005R\u0000\u0000\u07e3\u086a\u0001\u0000\u0000"+
		"\u0000\u07e4\u07e5\u0005)\u0000\u0000\u07e5\u07e6\u0005\u0002\u0000\u0000"+
		"\u07e6\u07e7\u0003`0\u0000\u07e7\u07e8\u0005\u001f\u0000\u0000\u07e8\u07e9"+
		"\u0003\u0080@\u0000\u07e9\u07ea\u0005\u0003\u0000\u0000\u07ea\u086a\u0001"+
		"\u0000\u0000\u0000\u07eb\u07ec\u0005\u00f1\u0000\u0000\u07ec\u07ed\u0005"+
		"\u0002\u0000\u0000\u07ed\u07ee\u0003`0\u0000\u07ee\u07ef\u0005\u001f\u0000"+
		"\u0000\u07ef\u07f0\u0003\u0080@\u0000\u07f0\u07f1\u0005\u0003\u0000\u0000"+
		"\u07f1\u086a\u0001\u0000\u0000\u0000\u07f2\u07f3\u0005)\u0000\u0000\u07f3"+
		"\u07f4\u0005\u0002\u0000\u0000\u07f4\u07f5\u0003`0\u0000\u07f5\u07f8\u0005"+
		"\u001f\u0000\u0000\u07f6\u07f7\u0005\u0120\u0000\u0000\u07f7\u07f9\u0005"+
		"\u0001\u0000\u0000\u07f8\u07f6\u0001\u0000\u0000\u0000\u07f8\u07f9\u0001"+
		"\u0000\u0000\u0000\u07f9\u07fa\u0001\u0000\u0000\u0000\u07fa\u07fb\u0003"+
		"\u0080@\u0000\u07fb\u07fc\u0005\u0003\u0000\u0000\u07fc\u086a\u0001\u0000"+
		"\u0000\u0000\u07fd\u07fe\u0005\u001e\u0000\u0000\u07fe\u0807\u0005\f\u0000"+
		"\u0000\u07ff\u0804\u0003`0\u0000\u0800\u0801\u0005\u0004\u0000\u0000\u0801"+
		"\u0803\u0003`0\u0000\u0802\u0800\u0001\u0000\u0000\u0000\u0803\u0806\u0001"+
		"\u0000\u0000\u0000\u0804\u0802\u0001\u0000\u0000\u0000\u0804\u0805\u0001"+
		"\u0000\u0000\u0000\u0805\u0808\u0001\u0000\u0000\u0000\u0806\u0804\u0001"+
		"\u0000\u0000\u0000\u0807\u07ff\u0001\u0000\u0000\u0000\u0807\u0808\u0001"+
		"\u0000\u0000\u0000\u0808\u0809\u0001\u0000\u0000\u0000\u0809\u086a\u0005"+
		"\r\u0000\u0000\u080a\u0813\u0005\f\u0000\u0000\u080b\u0810\u0003`0\u0000"+
		"\u080c\u080d\u0005\u0004\u0000\u0000\u080d\u080f\u0003`0\u0000\u080e\u080c"+
		"\u0001\u0000\u0000\u0000\u080f\u0812\u0001\u0000\u0000\u0000\u0810\u080e"+
		"\u0001\u0000\u0000\u0000\u0810\u0811\u0001\u0000\u0000\u0000\u0811\u0814"+
		"\u0001\u0000\u0000\u0000\u0812\u0810\u0001\u0000\u0000\u0000\u0813\u080b"+
		"\u0001\u0000\u0000\u0000\u0813\u0814\u0001\u0000\u0000\u0000\u0814\u0815"+
		"\u0001\u0000\u0000\u0000\u0815\u086a\u0005\r\u0000\u0000\u0816\u086a\u0003"+
		"\u00b6[\u0000\u0817\u086a\u00058\u0000\u0000\u0818\u081c\u0005<\u0000"+
		"\u0000\u0819\u081a\u0005\u0002\u0000\u0000\u081a\u081b\u0005\u011d\u0000"+
		"\u0000\u081b\u081d\u0005\u0003\u0000\u0000\u081c\u0819\u0001\u0000\u0000"+
		"\u0000\u081c\u081d\u0001\u0000\u0000\u0000\u081d\u086a\u0001\u0000\u0000"+
		"\u0000\u081e\u0822\u0005=\u0000\u0000\u081f\u0820\u0005\u0002\u0000\u0000"+
		"\u0820\u0821\u0005\u011d\u0000\u0000\u0821\u0823\u0005\u0003\u0000\u0000"+
		"\u0822\u081f\u0001\u0000\u0000\u0000\u0822\u0823\u0001\u0000\u0000\u0000"+
		"\u0823\u086a\u0001\u0000\u0000\u0000\u0824\u0828\u0005\u008a\u0000\u0000"+
		"\u0825\u0826\u0005\u0002\u0000\u0000\u0826\u0827\u0005\u011d\u0000\u0000"+
		"\u0827\u0829\u0005\u0003\u0000\u0000\u0828\u0825\u0001\u0000\u0000\u0000"+
		"\u0828\u0829\u0001\u0000\u0000\u0000\u0829\u086a\u0001\u0000\u0000\u0000"+
		"\u082a\u082e\u0005\u008b\u0000\u0000\u082b\u082c\u0005\u0002\u0000\u0000"+
		"\u082c\u082d\u0005\u011d\u0000\u0000\u082d\u082f\u0005\u0003\u0000\u0000"+
		"\u082e\u082b\u0001\u0000\u0000\u0000\u082e\u082f\u0001\u0000\u0000\u0000"+
		"\u082f\u086a\u0001\u0000\u0000\u0000\u0830\u086a\u0005>\u0000\u0000\u0831"+
		"\u086a\u00057\u0000\u0000\u0832\u0833\u0003\u00b6[\u0000\u0833\u0834\u0005"+
		"\u0001\u0000\u0000\u0834\u0836\u0001\u0000\u0000\u0000\u0835\u0832\u0001"+
		"\u0000\u0000\u0000\u0835\u0836\u0001\u0000\u0000\u0000\u0836\u0837\u0001"+
		"\u0000\u0000\u0000\u0837\u083a\u0005;\u0000\u0000\u0838\u0839\u0005\u0002"+
		"\u0000\u0000\u0839\u083b\u0005\u0003\u0000\u0000\u083a\u0838\u0001\u0000"+
		"\u0000\u0000\u083a\u083b\u0001\u0000\u0000\u0000\u083b\u086a\u0001\u0000"+
		"\u0000\u0000\u083c\u086a\u00059\u0000\u0000\u083d\u083e\u0005\u00e3\u0000"+
		"\u0000\u083e\u083f\u0005\u0002\u0000\u0000\u083f\u0840\u0003h4\u0000\u0840"+
		"\u0841\u0005d\u0000\u0000\u0841\u0844\u0003h4\u0000\u0842\u0843\u0005"+
		"b\u0000\u0000\u0843\u0845\u0003h4\u0000\u0844\u0842\u0001\u0000\u0000"+
		"\u0000\u0844\u0845\u0001\u0000\u0000\u0000\u0845\u0846\u0001\u0000\u0000"+
		"\u0000\u0846\u0847\u0005\u0003\u0000\u0000\u0847\u086a\u0001\u0000\u0000"+
		"\u0000\u0848\u0849\u0005\u009f\u0000\u0000\u0849\u084a\u0005\u0002\u0000"+
		"\u0000\u084a\u084d\u0003h4\u0000\u084b\u084c\u0005\u0004\u0000\u0000\u084c"+
		"\u084e\u0003~?\u0000\u084d\u084b\u0001\u0000\u0000\u0000\u084d\u084e\u0001"+
		"\u0000\u0000\u0000\u084e\u084f\u0001\u0000\u0000\u0000\u084f\u0850\u0005"+
		"\u0003\u0000\u0000\u0850\u086a\u0001\u0000\u0000\u0000\u0851\u0852\u0005"+
		"[\u0000\u0000\u0852\u0853\u0005\u0002\u0000\u0000\u0853\u0854\u0003\u00b6"+
		"[\u0000\u0854\u0855\u0005d\u0000\u0000\u0855\u0856\u0003h4\u0000\u0856"+
		"\u0857\u0005\u0003\u0000\u0000\u0857\u086a\u0001\u0000\u0000\u0000\u0858"+
		"\u0859\u0005\u0002\u0000\u0000\u0859\u085a\u0003`0\u0000\u085a\u085b\u0005"+
		"\u0003\u0000\u0000\u085b\u086a\u0001\u0000\u0000\u0000\u085c\u085d\u0005"+
		"l\u0000\u0000\u085d\u0866\u0005\u0002\u0000\u0000\u085e\u0863\u0003\u00aa"+
		"U\u0000\u085f\u0860\u0005\u0004\u0000\u0000\u0860\u0862\u0003\u00aaU\u0000"+
		"\u0861\u085f\u0001\u0000\u0000\u0000\u0862\u0865\u0001\u0000\u0000\u0000"+
		"\u0863\u0861\u0001\u0000\u0000\u0000\u0863\u0864\u0001\u0000\u0000\u0000"+
		"\u0864\u0867\u0001\u0000\u0000\u0000\u0865\u0863\u0001\u0000\u0000\u0000"+
		"\u0866\u085e\u0001\u0000\u0000\u0000\u0866\u0867\u0001\u0000\u0000\u0000"+
		"\u0867\u0868\u0001\u0000\u0000\u0000\u0868\u086a\u0005\u0003\u0000\u0000"+
		"\u0869\u0721\u0001\u0000\u0000\u0000\u0869\u0723\u0001\u0000\u0000\u0000"+
		"\u0869\u0724\u0001\u0000\u0000\u0000\u0869\u0727\u0001\u0000\u0000\u0000"+
		"\u0869\u072a\u0001\u0000\u0000\u0000\u0869\u0732\u0001\u0000\u0000\u0000"+
		"\u0869\u0733\u0001\u0000\u0000\u0000\u0869\u0734\u0001\u0000\u0000\u0000"+
		"\u0869\u0735\u0001\u0000\u0000\u0000\u0869\u0736\u0001\u0000\u0000\u0000"+
		"\u0869\u0737\u0001\u0000\u0000\u0000\u0869\u073e\u0001\u0000\u0000\u0000"+
		"\u0869\u0748\u0001\u0000\u0000\u0000\u0869\u0754\u0001\u0000\u0000\u0000"+
		"\u0869\u0774\u0001\u0000\u0000\u0000\u0869\u0786\u0001\u0000\u0000\u0000"+
		"\u0869\u07ad\u0001\u0000\u0000\u0000\u0869\u07b0\u0001\u0000\u0000\u0000"+
		"\u0869\u07b4\u0001\u0000\u0000\u0000\u0869\u07c2\u0001\u0000\u0000\u0000"+
		"\u0869\u07c6\u0001\u0000\u0000\u0000\u0869\u07cb\u0001\u0000\u0000\u0000"+
		"\u0869\u07d8\u0001\u0000\u0000\u0000\u0869\u07e4\u0001\u0000\u0000\u0000"+
		"\u0869\u07eb\u0001\u0000\u0000\u0000\u0869\u07f2\u0001\u0000\u0000\u0000"+
		"\u0869\u07fd\u0001\u0000\u0000\u0000\u0869\u080a\u0001\u0000\u0000\u0000"+
		"\u0869\u0816\u0001\u0000\u0000\u0000\u0869\u0817\u0001\u0000\u0000\u0000"+
		"\u0869\u0818\u0001\u0000\u0000\u0000\u0869\u081e\u0001\u0000\u0000\u0000"+
		"\u0869\u0824\u0001\u0000\u0000\u0000\u0869\u082a\u0001\u0000\u0000\u0000"+
		"\u0869\u0830\u0001\u0000\u0000\u0000\u0869\u0831\u0001\u0000\u0000\u0000"+
		"\u0869\u0835\u0001\u0000\u0000\u0000\u0869\u083c\u0001\u0000\u0000\u0000"+
		"\u0869\u083d\u0001\u0000\u0000\u0000\u0869\u0848\u0001\u0000\u0000\u0000"+
		"\u0869\u0851\u0001\u0000\u0000\u0000\u0869\u0858\u0001\u0000\u0000\u0000"+
		"\u0869\u085c\u0001\u0000\u0000\u0000\u086a\u087c\u0001\u0000\u0000\u0000"+
		"\u086b\u086c\n\u0014\u0000\u0000\u086c\u086f\u0005\u0128\u0000\u0000\u086d"+
		"\u086e\u0005\u0120\u0000\u0000\u086e\u0870\u0005\u0001\u0000\u0000\u086f"+
		"\u086d\u0001\u0000\u0000\u0000\u086f\u0870\u0001\u0000\u0000\u0000\u0870"+
		"\u0871\u0001\u0000\u0000\u0000\u0871\u087b\u0003\u0080@\u0000\u0872\u0873"+
		"\n\u0011\u0000\u0000\u0873\u0874\u0005\f\u0000\u0000\u0874\u0875\u0003"+
		"h4\u0000\u0875\u0876\u0005\r\u0000\u0000\u0876\u087b\u0001\u0000\u0000"+
		"\u0000\u0877\u0878\n\u000f\u0000\u0000\u0878\u0879\u0005\u0001\u0000\u0000"+
		"\u0879\u087b\u0003\u00b6[\u0000\u087a\u086b\u0001\u0000\u0000\u0000\u087a"+
		"\u0872\u0001\u0000\u0000\u0000\u087a\u0877\u0001\u0000\u0000\u0000\u087b"+
		"\u087e\u0001\u0000\u0000\u0000\u087c\u087a\u0001\u0000\u0000\u0000\u087c"+
		"\u087d\u0001\u0000\u0000\u0000\u087dk\u0001\u0000\u0000\u0000\u087e\u087c"+
		"\u0001\u0000\u0000\u0000\u087f\u0880\u0007\u0013\u0000\u0000\u0880m\u0001"+
		"\u0000\u0000\u0000\u0881\u0882\u0005q\u0000\u0000\u0882\u0886\u0005\u00a3"+
		"\u0000\u0000\u0883\u0884\u0005\u00c8\u0000\u0000\u0884\u0886\u0005\u00a3"+
		"\u0000\u0000\u0885\u0881\u0001\u0000\u0000\u0000\u0885\u0883\u0001\u0000"+
		"\u0000\u0000\u0886o\u0001\u0000\u0000\u0000\u0887\u088f\u0005\u011a\u0000"+
		"\u0000\u0888\u088b\u0005\u011b\u0000\u0000\u0889\u088a\u0005\u00f3\u0000"+
		"\u0000\u088a\u088c\u0005\u011a\u0000\u0000\u088b\u0889\u0001\u0000\u0000"+
		"\u0000\u088b\u088c\u0001\u0000\u0000\u0000\u088c\u088f\u0001\u0000\u0000"+
		"\u0000\u088d\u088f\u0005\u0129\u0000\u0000\u088e\u0887\u0001\u0000\u0000"+
		"\u0000\u088e\u0888\u0001\u0000\u0000\u0000\u088e\u088d\u0001\u0000\u0000"+
		"\u0000\u088fq\u0001\u0000\u0000\u0000\u0890\u0891\u0005\u00eb\u0000\u0000"+
		"\u0891\u0892\u0005\u010b\u0000\u0000\u0892\u0897\u0003z=\u0000\u0893\u0894"+
		"\u0005\u00eb\u0000\u0000\u0894\u0895\u0005\u010b\u0000\u0000\u0895\u0897"+
		"\u0003p8\u0000\u0896\u0890\u0001\u0000\u0000\u0000\u0896\u0893\u0001\u0000"+
		"\u0000\u0000\u0897s\u0001\u0000\u0000\u0000\u0898\u0899\u0007\u0014\u0000"+
		"\u0000\u0899u\u0001\u0000\u0000\u0000\u089a\u089b\u0007\u0015\u0000\u0000"+
		"\u089bw\u0001\u0000\u0000\u0000\u089c\u089d\u0007\u0016\u0000\u0000\u089d"+
		"y\u0001\u0000\u0000\u0000\u089e\u08a0\u0005z\u0000\u0000\u089f\u08a1\u0007"+
		"\u0010\u0000\u0000\u08a0\u089f\u0001\u0000\u0000\u0000\u08a0\u08a1\u0001"+
		"\u0000\u0000\u0000\u08a1\u08a2\u0001\u0000\u0000\u0000\u08a2\u08a3\u0003"+
		"p8\u0000\u08a3\u08a6\u0003|>\u0000\u08a4\u08a5\u0005\u00ed\u0000\u0000"+
		"\u08a5\u08a7\u0003|>\u0000\u08a6\u08a4\u0001\u0000\u0000\u0000\u08a6\u08a7"+
		"\u0001\u0000\u0000\u0000\u08a7{\u0001\u0000\u0000\u0000\u08a8\u08a9\u0007"+
		"\u0017\u0000\u0000\u08a9}\u0001\u0000\u0000\u0000\u08aa\u08ab\u0007\u0018"+
		"\u0000\u0000\u08ab\u007f\u0001\u0000\u0000\u0000\u08ac\u08ad\u0006@\uffff"+
		"\uffff\u0000\u08ad\u08ae\u0005\u00d0\u0000\u0000\u08ae\u08af\u0005\u0002"+
		"\u0000\u0000\u08af\u08b4\u0003\u0082A\u0000\u08b0\u08b1\u0005\u0004\u0000"+
		"\u0000\u08b1\u08b3\u0003\u0082A\u0000\u08b2\u08b0\u0001\u0000\u0000\u0000"+
		"\u08b3\u08b6\u0001\u0000\u0000\u0000\u08b4\u08b2\u0001\u0000\u0000\u0000"+
		"\u08b4\u08b5\u0001\u0000\u0000\u0000\u08b5\u08b7\u0001\u0000\u0000\u0000"+
		"\u08b6\u08b4\u0001\u0000\u0000\u0000\u08b7\u08b8\u0005\u0003\u0000\u0000"+
		"\u08b8\u0908\u0001\u0000\u0000\u0000\u08b9\u08ba\u0005z\u0000\u0000\u08ba"+
		"\u08bd\u0003|>\u0000\u08bb\u08bc\u0005\u00ed\u0000\u0000\u08bc\u08be\u0003"+
		"|>\u0000\u08bd\u08bb\u0001\u0000\u0000\u0000\u08bd\u08be\u0001\u0000\u0000"+
		"\u0000\u08be\u0908\u0001\u0000\u0000\u0000\u08bf\u08c4\u0005\u00ec\u0000"+
		"\u0000\u08c0\u08c1\u0005\u0002\u0000\u0000\u08c1\u08c2\u0003\u0084B\u0000"+
		"\u08c2\u08c3\u0005\u0003\u0000\u0000\u08c3\u08c5\u0001\u0000\u0000\u0000"+
		"\u08c4\u08c0\u0001\u0000\u0000\u0000\u08c4\u08c5\u0001\u0000";
	private static final String _serializedATNSegment1 =
		"\u0000\u0000\u08c5\u08c9\u0001\u0000\u0000\u0000\u08c6\u08c7\u0005\u0107"+
		"\u0000\u0000\u08c7\u08c8\u0005\u00eb\u0000\u0000\u08c8\u08ca\u0005\u010b"+
		"\u0000\u0000\u08c9\u08c6\u0001\u0000\u0000\u0000\u08c9\u08ca\u0001\u0000"+
		"\u0000\u0000\u08ca\u0908\u0001\u0000\u0000\u0000\u08cb\u08d0\u0005\u00ec"+
		"\u0000\u0000\u08cc\u08cd\u0005\u0002\u0000\u0000\u08cd\u08ce\u0003\u0084"+
		"B\u0000\u08ce\u08cf\u0005\u0003\u0000\u0000\u08cf\u08d1\u0001\u0000\u0000"+
		"\u0000\u08d0\u08cc\u0001\u0000\u0000\u0000\u08d0\u08d1\u0001\u0000\u0000"+
		"\u0000\u08d1\u08d2\u0001\u0000\u0000\u0000\u08d2\u08d3\u0005\u0105\u0000"+
		"\u0000\u08d3\u08d4\u0005\u00eb\u0000\u0000\u08d4\u0908\u0005\u010b\u0000"+
		"\u0000\u08d5\u08da\u0005\u00eb\u0000\u0000\u08d6\u08d7\u0005\u0002\u0000"+
		"\u0000\u08d7\u08d8\u0003\u0084B\u0000\u08d8\u08d9\u0005\u0003\u0000\u0000"+
		"\u08d9\u08db\u0001\u0000\u0000\u0000\u08da\u08d6\u0001\u0000\u0000\u0000"+
		"\u08da\u08db\u0001\u0000\u0000\u0000\u08db\u08df\u0001\u0000\u0000\u0000"+
		"\u08dc\u08dd\u0005\u0107\u0000\u0000\u08dd\u08de\u0005\u00eb\u0000\u0000"+
		"\u08de\u08e0\u0005\u010b\u0000\u0000\u08df\u08dc\u0001\u0000\u0000\u0000"+
		"\u08df\u08e0\u0001\u0000\u0000\u0000\u08e0\u0908\u0001\u0000\u0000\u0000"+
		"\u08e1\u08e6\u0005\u00eb\u0000\u0000\u08e2\u08e3\u0005\u0002\u0000\u0000"+
		"\u08e3\u08e4\u0003\u0084B\u0000\u08e4\u08e5\u0005\u0003\u0000\u0000\u08e5"+
		"\u08e7\u0001\u0000\u0000\u0000\u08e6\u08e2\u0001\u0000\u0000\u0000\u08e6"+
		"\u08e7\u0001\u0000\u0000\u0000\u08e7\u08e8\u0001\u0000\u0000\u0000\u08e8"+
		"\u08e9\u0005\u0105\u0000\u0000\u08e9\u08ea\u0005\u00eb\u0000\u0000\u08ea"+
		"\u0908\u0005\u010b\u0000\u0000\u08eb\u08ec\u0005N\u0000\u0000\u08ec\u0908"+
		"\u0005\u00bc\u0000\u0000\u08ed\u08ee\u0005\u001e\u0000\u0000\u08ee\u08ef"+
		"\u0005\u010e\u0000\u0000\u08ef\u08f0\u0003\u0080@\u0000\u08f0\u08f1\u0005"+
		"\u0110\u0000\u0000\u08f1\u0908\u0001\u0000\u0000\u0000\u08f2\u08f3\u0005"+
		"\u008d\u0000\u0000\u08f3\u08f4\u0005\u010e\u0000\u0000\u08f4\u08f5\u0003"+
		"\u0080@\u0000\u08f5\u08f6\u0005\u0004\u0000\u0000\u08f6\u08f7\u0003\u0080"+
		"@\u0000\u08f7\u08f8\u0005\u0110\u0000\u0000\u08f8\u0908\u0001\u0000\u0000"+
		"\u0000\u08f9\u0905\u0003\u00b6[\u0000\u08fa\u08fb\u0005\u0002\u0000\u0000"+
		"\u08fb\u0900\u0003\u0084B\u0000\u08fc\u08fd\u0005\u0004\u0000\u0000\u08fd"+
		"\u08ff\u0003\u0084B\u0000\u08fe\u08fc\u0001\u0000\u0000\u0000\u08ff\u0902"+
		"\u0001\u0000\u0000\u0000\u0900\u08fe\u0001\u0000\u0000\u0000\u0900\u0901"+
		"\u0001\u0000\u0000\u0000\u0901\u0903\u0001\u0000\u0000\u0000\u0902\u0900"+
		"\u0001\u0000\u0000\u0000\u0903\u0904\u0005\u0003\u0000\u0000\u0904\u0906"+
		"\u0001\u0000\u0000\u0000\u0905\u08fa\u0001\u0000\u0000\u0000\u0905\u0906"+
		"\u0001\u0000\u0000\u0000\u0906\u0908\u0001\u0000\u0000\u0000\u0907\u08ac"+
		"\u0001\u0000\u0000\u0000\u0907\u08b9\u0001\u0000\u0000\u0000\u0907\u08bf"+
		"\u0001\u0000\u0000\u0000\u0907\u08cb\u0001\u0000\u0000\u0000\u0907\u08d5"+
		"\u0001\u0000\u0000\u0000\u0907\u08e1\u0001\u0000\u0000\u0000\u0907\u08eb"+
		"\u0001\u0000\u0000\u0000\u0907\u08ed\u0001\u0000\u0000\u0000\u0907\u08f2"+
		"\u0001\u0000\u0000\u0000\u0907\u08f9\u0001\u0000\u0000\u0000\u0908\u0912"+
		"\u0001\u0000\u0000\u0000\u0909\u090a\n\u0002\u0000\u0000\u090a\u090e\u0005"+
		"\u001e\u0000\u0000\u090b\u090c\u0005\f\u0000\u0000\u090c\u090d\u0005\u011d"+
		"\u0000\u0000\u090d\u090f\u0005\r\u0000\u0000\u090e\u090b\u0001\u0000\u0000"+
		"\u0000\u090e\u090f\u0001\u0000\u0000\u0000\u090f\u0911\u0001\u0000\u0000"+
		"\u0000\u0910\u0909\u0001\u0000\u0000\u0000\u0911\u0914\u0001\u0000\u0000"+
		"\u0000\u0912\u0910\u0001\u0000\u0000\u0000\u0912\u0913\u0001\u0000\u0000"+
		"\u0000\u0913\u0081\u0001\u0000\u0000\u0000\u0914\u0912\u0001\u0000\u0000"+
		"\u0000\u0915\u091a\u0003\u0080@\u0000\u0916\u0917\u0003\u00b6[\u0000\u0917"+
		"\u0918\u0003\u0080@\u0000\u0918\u091a\u0001\u0000\u0000\u0000\u0919\u0915"+
		"\u0001\u0000\u0000\u0000\u0919\u0916\u0001\u0000\u0000\u0000\u091a\u0083"+
		"\u0001\u0000\u0000\u0000\u091b\u091e\u0005\u011d\u0000\u0000\u091c\u091e"+
		"\u0003\u0080@\u0000\u091d\u091b\u0001\u0000\u0000\u0000\u091d\u091c\u0001"+
		"\u0000\u0000\u0000\u091e\u0085\u0001\u0000\u0000\u0000\u091f\u0920\u0005"+
		"\u0102\u0000\u0000\u0920\u0921\u0003`0\u0000\u0921\u0922\u0005\u00e9\u0000"+
		"\u0000\u0922\u0923\u0003`0\u0000\u0923\u0087\u0001\u0000\u0000\u0000\u0924"+
		"\u0925\u0005^\u0000\u0000\u0925\u0926\u0005\u0002\u0000\u0000\u0926\u0927"+
		"\u0005\u0103\u0000\u0000\u0927\u0928\u0003b1\u0000\u0928\u0929\u0005\u0003"+
		"\u0000\u0000\u0929\u0089\u0001\u0000\u0000\u0000\u092a\u092b\u0005\u0102"+
		"\u0000\u0000\u092b\u092e\u0005\u008f\u0000\u0000\u092c\u092d\u0005\u001c"+
		"\u0000\u0000\u092d\u092f\u0003`0\u0000\u092e\u092c\u0001\u0000\u0000\u0000"+
		"\u092e\u092f\u0001\u0000\u0000\u0000\u092f\u0930\u0001\u0000\u0000\u0000"+
		"\u0930\u0931\u0005\u00e9\u0000\u0000\u0931\u0932\u0005\u00f9\u0000\u0000"+
		"\u0932\u0933\u0005\u00dc\u0000\u0000\u0933\u0934\u0003\u00b6[\u0000\u0934"+
		"\u0935\u0005\u010c\u0000\u0000\u0935\u093d\u0003`0\u0000\u0936\u0937\u0005"+
		"\u0004\u0000\u0000\u0937\u0938\u0003\u00b6[\u0000\u0938\u0939\u0005\u010c"+
		"\u0000\u0000\u0939\u093a\u0003`0\u0000\u093a\u093c\u0001\u0000\u0000\u0000"+
		"\u093b\u0936\u0001\u0000\u0000\u0000\u093c\u093f\u0001\u0000\u0000\u0000"+
		"\u093d\u093b\u0001\u0000\u0000\u0000\u093d\u093e\u0001\u0000\u0000\u0000"+
		"\u093e\u096b\u0001\u0000\u0000\u0000\u093f\u093d\u0001\u0000\u0000\u0000"+
		"\u0940\u0941\u0005\u0102\u0000\u0000\u0941\u0944\u0005\u008f\u0000\u0000"+
		"\u0942\u0943\u0005\u001c\u0000\u0000\u0943\u0945\u0003`0\u0000\u0944\u0942"+
		"\u0001\u0000\u0000\u0000\u0944\u0945\u0001\u0000\u0000\u0000\u0945\u0946"+
		"\u0001\u0000\u0000\u0000\u0946\u0947\u0005\u00e9\u0000\u0000\u0947\u096b"+
		"\u0005G\u0000\u0000\u0948\u0949\u0005\u0102\u0000\u0000\u0949\u094a\u0005"+
		"\u00a0\u0000\u0000\u094a\u094d\u0005\u008f\u0000\u0000\u094b\u094c\u0005"+
		"\u001c\u0000\u0000\u094c\u094e\u0003`0\u0000\u094d\u094b\u0001\u0000\u0000"+
		"\u0000\u094d\u094e\u0001\u0000\u0000\u0000\u094e\u094f\u0001\u0000\u0000"+
		"\u0000\u094f\u0950\u0005\u00e9\u0000\u0000\u0950\u095c\u0005x\u0000\u0000"+
		"\u0951\u0952\u0005\u0002\u0000\u0000\u0952\u0957\u0003\u00b6[\u0000\u0953"+
		"\u0954\u0005\u0004\u0000\u0000\u0954\u0956\u0003\u00b6[\u0000\u0955\u0953"+
		"\u0001\u0000\u0000\u0000\u0956\u0959\u0001\u0000\u0000\u0000\u0957\u0955"+
		"\u0001\u0000\u0000\u0000\u0957\u0958\u0001\u0000\u0000\u0000\u0958\u095a"+
		"\u0001\u0000\u0000\u0000\u0959\u0957\u0001\u0000\u0000\u0000\u095a\u095b"+
		"\u0005\u0003\u0000\u0000\u095b\u095d\u0001\u0000\u0000\u0000\u095c\u0951"+
		"\u0001\u0000\u0000\u0000\u095c\u095d\u0001\u0000\u0000\u0000\u095d\u095e"+
		"\u0001\u0000\u0000\u0000\u095e\u095f\u0005\u00fe\u0000\u0000\u095f\u0960"+
		"\u0005\u0002\u0000\u0000\u0960\u0965\u0003`0\u0000\u0961\u0962\u0005\u0004"+
		"\u0000\u0000\u0962\u0964\u0003`0\u0000\u0963\u0961\u0001\u0000\u0000\u0000"+
		"\u0964\u0967\u0001\u0000\u0000\u0000\u0965\u0963\u0001\u0000\u0000\u0000"+
		"\u0965\u0966\u0001\u0000\u0000\u0000\u0966\u0968\u0001\u0000\u0000\u0000"+
		"\u0967\u0965\u0001\u0000\u0000\u0000\u0968\u0969\u0005\u0003\u0000\u0000"+
		"\u0969\u096b\u0001\u0000\u0000\u0000\u096a\u092a\u0001\u0000\u0000\u0000"+
		"\u096a\u0940\u0001\u0000\u0000\u0000\u096a\u0948\u0001\u0000\u0000\u0000"+
		"\u096b\u008b\u0001\u0000\u0000\u0000\u096c\u0972\u0005\u00b1\u0000\u0000"+
		"\u096d\u0973\u0003\u00b6[\u0000\u096e\u096f\u0005\u0002\u0000\u0000\u096f"+
		"\u0970\u00036\u001b\u0000\u0970\u0971\u0005\u0003\u0000\u0000\u0971\u0973"+
		"\u0001\u0000\u0000\u0000\u0972\u096d\u0001\u0000\u0000\u0000\u0972\u096e"+
		"\u0001\u0000\u0000\u0000\u0973\u008d\u0001\u0000\u0000\u0000\u0974\u0975"+
		"\u0005\u0093\u0000\u0000\u0975\u097a\u0003N\'\u0000\u0976\u0977\u0005"+
		"\u0004\u0000\u0000\u0977\u0979\u0003N\'\u0000\u0978\u0976\u0001\u0000"+
		"\u0000\u0000\u0979\u097c\u0001\u0000\u0000\u0000\u097a\u0978\u0001\u0000"+
		"\u0000\u0000\u097a\u097b\u0001\u0000\u0000\u0000\u097b\u097e\u0001\u0000"+
		"\u0000\u0000\u097c\u097a\u0001\u0000\u0000\u0000\u097d\u0974\u0001\u0000"+
		"\u0000\u0000\u097d\u097e\u0001\u0000\u0000\u0000\u097e\u097f\u0001\u0000"+
		"\u0000\u0000\u097f\u0983\u0003\u0090H\u0000\u0980\u0981\u0005\u0018\u0000"+
		"\u0000\u0981\u0982\u0005\u008e\u0000\u0000\u0982\u0984\u0003T*\u0000\u0983"+
		"\u0980\u0001\u0000\u0000\u0000\u0983\u0984\u0001\u0000\u0000\u0000\u0984"+
		"\u0986\u0001\u0000\u0000\u0000\u0985\u0987\u0007\u000f\u0000\u0000\u0986"+
		"\u0985\u0001\u0000\u0000\u0000\u0986\u0987\u0001\u0000\u0000\u0000\u0987"+
		"\u098d\u0001\u0000\u0000\u0000\u0988\u0989\u0005\u00b7\u0000\u0000\u0989"+
		"\u098a\u0005\u0002\u0000\u0000\u098a\u098b\u0003\u0094J\u0000\u098b\u098c"+
		"\u0005\u0003\u0000\u0000\u098c\u098e\u0001\u0000\u0000\u0000\u098d\u0988"+
		"\u0001\u0000\u0000\u0000\u098d\u098e\u0001\u0000\u0000\u0000\u098e\u0998"+
		"\u0001\u0000\u0000\u0000\u098f\u0990\u0005\u00e2\u0000\u0000\u0990\u0995"+
		"\u0003V+\u0000\u0991\u0992\u0005\u0004\u0000\u0000\u0992\u0994\u0003V"+
		"+\u0000\u0993\u0991\u0001\u0000\u0000\u0000\u0994\u0997\u0001\u0000\u0000"+
		"\u0000\u0995\u0993\u0001\u0000\u0000\u0000\u0995\u0996\u0001\u0000\u0000"+
		"\u0000\u0996\u0999\u0001\u0000\u0000\u0000\u0997\u0995\u0001\u0000\u0000"+
		"\u0000\u0998\u098f\u0001\u0000\u0000\u0000\u0998\u0999\u0001\u0000\u0000"+
		"\u0000\u0999\u09a3\u0001\u0000\u0000\u0000\u099a\u099b\u0005K\u0000\u0000"+
		"\u099b\u09a0\u0003X,\u0000\u099c\u099d\u0005\u0004\u0000\u0000\u099d\u099f"+
		"\u0003X,\u0000\u099e\u099c\u0001\u0000\u0000\u0000\u099f\u09a2\u0001\u0000"+
		"\u0000\u0000\u09a0\u099e\u0001\u0000\u0000\u0000\u09a0\u09a1\u0001\u0000"+
		"\u0000\u0000\u09a1\u09a4\u0001\u0000\u0000\u0000\u09a2\u09a0\u0001\u0000"+
		"\u0000\u0000\u09a3\u099a\u0001\u0000\u0000\u0000\u09a3\u09a4\u0001\u0000"+
		"\u0000\u0000\u09a4\u008f\u0001\u0000\u0000\u0000\u09a5\u09a6\u0005\u00c0"+
		"\u0000\u0000\u09a6\u09be\u0003\u0092I\u0000\u09a7\u09a8\u0005\u00d1\u0000"+
		"\u0000\u09a8\u09be\u0003\u0092I\u0000\u09a9\u09aa\u0005m\u0000\u0000\u09aa"+
		"\u09be\u0003\u0092I\u0000\u09ab\u09ac\u0005\u00c0\u0000\u0000\u09ac\u09ad"+
		"\u0005$\u0000\u0000\u09ad\u09ae\u0003\u0092I\u0000\u09ae\u09af\u0005\u001c"+
		"\u0000\u0000\u09af\u09b0\u0003\u0092I\u0000\u09b0\u09be\u0001\u0000\u0000"+
		"\u0000\u09b1\u09b2\u0005\u00d1\u0000\u0000\u09b2\u09b3\u0005$\u0000\u0000"+
		"\u09b3\u09b4\u0003\u0092I\u0000\u09b4\u09b5\u0005\u001c\u0000\u0000\u09b5"+
		"\u09b6\u0003\u0092I\u0000\u09b6\u09be\u0001\u0000\u0000\u0000\u09b7\u09b8"+
		"\u0005m\u0000\u0000\u09b8\u09b9\u0005$\u0000\u0000\u09b9\u09ba\u0003\u0092"+
		"I\u0000\u09ba\u09bb\u0005\u001c\u0000\u0000\u09bb\u09bc\u0003\u0092I\u0000"+
		"\u09bc\u09be\u0001\u0000\u0000\u0000\u09bd\u09a5\u0001\u0000\u0000\u0000"+
		"\u09bd\u09a7\u0001\u0000\u0000\u0000\u09bd\u09a9\u0001\u0000\u0000\u0000"+
		"\u09bd\u09ab\u0001\u0000\u0000\u0000\u09bd\u09b1\u0001\u0000\u0000\u0000"+
		"\u09bd\u09b7\u0001\u0000\u0000\u0000\u09be\u0091\u0001\u0000\u0000\u0000"+
		"\u09bf\u09c0\u0005\u00f4\u0000\u0000\u09c0\u09c9\u0005\u00bb\u0000\u0000"+
		"\u09c1\u09c2\u0005\u00f4\u0000\u0000\u09c2\u09c9\u0005a\u0000\u0000\u09c3"+
		"\u09c4\u00056\u0000\u0000\u09c4\u09c9\u0005\u00d0\u0000\u0000\u09c5\u09c6"+
		"\u0003`0\u0000\u09c6\u09c7\u0007\u0019\u0000\u0000\u09c7\u09c9\u0001\u0000"+
		"\u0000\u0000\u09c8\u09bf\u0001\u0000\u0000\u0000\u09c8\u09c1\u0001\u0000"+
		"\u0000\u0000\u09c8\u09c3\u0001\u0000\u0000\u0000\u09c8\u09c5\u0001\u0000"+
		"\u0000\u0000\u09c9\u0093\u0001\u0000\u0000\u0000\u09ca\u09cb\u0006J\uffff"+
		"\uffff\u0000\u09cb\u09cd\u0003\u0096K\u0000\u09cc\u09ce\u0003\u0098L\u0000"+
		"\u09cd\u09cc\u0001\u0000\u0000\u0000\u09cd\u09ce\u0001\u0000\u0000\u0000"+
		"\u09ce\u09d6\u0001\u0000\u0000\u0000\u09cf\u09d0\n\u0002\u0000\u0000\u09d0"+
		"\u09d5\u0003\u0094J\u0003\u09d1\u09d2\n\u0001\u0000\u0000\u09d2\u09d3"+
		"\u0005\u000e\u0000\u0000\u09d3\u09d5\u0003\u0094J\u0002\u09d4\u09cf\u0001"+
		"\u0000\u0000\u0000\u09d4\u09d1\u0001\u0000\u0000\u0000\u09d5\u09d8\u0001"+
		"\u0000\u0000\u0000\u09d6\u09d4\u0001\u0000\u0000\u0000\u09d6\u09d7\u0001"+
		"\u0000\u0000\u0000\u09d7\u0095\u0001\u0000\u0000\u0000\u09d8\u09d6\u0001"+
		"\u0000\u0000\u0000\u09d9\u09f3\u0003\u00b6[\u0000\u09da\u09db\u0005\u0002"+
		"\u0000\u0000\u09db\u09f3\u0005\u0003\u0000\u0000\u09dc\u09dd\u0005\u00b9"+
		"\u0000\u0000\u09dd\u09de\u0005\u0002\u0000\u0000\u09de\u09e3\u0003\u0094"+
		"J\u0000\u09df\u09e0\u0005\u0004\u0000\u0000\u09e0\u09e2\u0003\u0094J\u0000"+
		"\u09e1\u09df\u0001\u0000\u0000\u0000\u09e2\u09e5\u0001\u0000\u0000\u0000"+
		"\u09e3\u09e1\u0001\u0000\u0000\u0000\u09e3\u09e4\u0001\u0000\u0000\u0000"+
		"\u09e4\u09e6\u0001\u0000\u0000\u0000\u09e5\u09e3\u0001\u0000\u0000\u0000"+
		"\u09e6\u09e7\u0005\u0003\u0000\u0000\u09e7\u09f3\u0001\u0000\u0000\u0000"+
		"\u09e8\u09e9\u0005\u0002\u0000\u0000\u09e9\u09ea\u0003\u0094J\u0000\u09ea"+
		"\u09eb\u0005\u0003\u0000\u0000\u09eb\u09f3\u0001\u0000\u0000\u0000\u09ec"+
		"\u09f3\u0005\u000f\u0000\u0000\u09ed\u09f3\u0005\u0010\u0000\u0000\u09ee"+
		"\u09ef\u0005\u0011\u0000\u0000\u09ef\u09f0\u0003\u0094J\u0000\u09f0\u09f1"+
		"\u0005\u0012\u0000\u0000\u09f1\u09f3\u0001\u0000\u0000\u0000\u09f2\u09d9"+
		"\u0001\u0000\u0000\u0000\u09f2\u09da\u0001\u0000\u0000\u0000\u09f2\u09dc"+
		"\u0001\u0000\u0000\u0000\u09f2\u09e8\u0001\u0000\u0000\u0000\u09f2\u09ec"+
		"\u0001\u0000\u0000\u0000\u09f2\u09ed\u0001\u0000\u0000\u0000\u09f2\u09ee"+
		"\u0001\u0000\u0000\u0000\u09f3\u0097\u0001\u0000\u0000\u0000\u09f4\u09f6"+
		"\u0005\u0114\u0000\u0000\u09f5\u09f7\u0005\u0118\u0000\u0000\u09f6\u09f5"+
		"\u0001\u0000\u0000\u0000\u09f6\u09f7\u0001\u0000\u0000\u0000\u09f7\u0a13"+
		"\u0001\u0000\u0000\u0000\u09f8\u09fa\u0005\u0112\u0000\u0000\u09f9\u09fb"+
		"\u0005\u0118\u0000\u0000\u09fa\u09f9\u0001\u0000\u0000\u0000\u09fa\u09fb"+
		"\u0001\u0000\u0000\u0000\u09fb\u0a13\u0001\u0000\u0000\u0000\u09fc\u09fe"+
		"\u0005\u0118\u0000\u0000\u09fd\u09ff\u0005\u0118\u0000\u0000\u09fe\u09fd"+
		"\u0001\u0000\u0000\u0000\u09fe\u09ff\u0001\u0000\u0000\u0000\u09ff\u0a13"+
		"\u0001\u0000\u0000\u0000\u0a00\u0a01\u0005\u0013\u0000\u0000\u0a01\u0a02"+
		"\u0005\u011d\u0000\u0000\u0a02\u0a04\u0005\u0014\u0000\u0000\u0a03\u0a05"+
		"\u0005\u0118\u0000\u0000\u0a04\u0a03\u0001\u0000\u0000\u0000\u0a04\u0a05"+
		"\u0001\u0000\u0000\u0000\u0a05\u0a13\u0001\u0000\u0000\u0000\u0a06\u0a08"+
		"\u0005\u0013\u0000\u0000\u0a07\u0a09\u0005\u011d\u0000\u0000\u0a08\u0a07"+
		"\u0001\u0000\u0000\u0000\u0a08\u0a09\u0001\u0000\u0000\u0000\u0a09\u0a0a"+
		"\u0001\u0000\u0000\u0000\u0a0a\u0a0c\u0005\u0004\u0000\u0000\u0a0b\u0a0d"+
		"\u0005\u011d\u0000\u0000\u0a0c\u0a0b\u0001\u0000\u0000\u0000\u0a0c\u0a0d"+
		"\u0001\u0000\u0000\u0000\u0a0d\u0a0e\u0001\u0000\u0000\u0000\u0a0e\u0a10"+
		"\u0005\u0014\u0000\u0000\u0a0f\u0a11\u0005\u0118\u0000\u0000\u0a10\u0a0f"+
		"\u0001\u0000\u0000\u0000\u0a10\u0a11\u0001\u0000\u0000\u0000\u0a11\u0a13"+
		"\u0001\u0000\u0000\u0000\u0a12\u09f4\u0001\u0000\u0000\u0000\u0a12\u09f8"+
		"\u0001\u0000\u0000\u0000\u0a12\u09fc\u0001\u0000\u0000\u0000\u0a12\u0a00"+
		"\u0001\u0000\u0000\u0000\u0a12\u0a06\u0001\u0000\u0000\u0000\u0a13\u0099"+
		"\u0001\u0000\u0000\u0000\u0a14\u0a15\u0003\u00b6[\u0000\u0a15\u0a16\u0005"+
		"\u010c\u0000\u0000\u0a16\u0a17\u0003`0\u0000\u0a17\u009b\u0001\u0000\u0000"+
		"\u0000\u0a18\u0a19\u0005c\u0000\u0000\u0a19\u0a1d\u0007\u001a\u0000\u0000"+
		"\u0a1a\u0a1b\u0005\u00f2\u0000\u0000\u0a1b\u0a1d\u0007\u001b\u0000\u0000"+
		"\u0a1c\u0a18\u0001\u0000\u0000\u0000\u0a1c\u0a1a\u0001\u0000\u0000\u0000"+
		"\u0a1d\u009d\u0001\u0000\u0000\u0000\u0a1e\u0a1f\u0005\u007f\u0000\u0000"+
		"\u0a1f\u0a20\u0005\u0085\u0000\u0000\u0a20\u0a24\u0003\u00a0P\u0000\u0a21"+
		"\u0a22\u0005\u00c1\u0000\u0000\u0a22\u0a24\u0007\u001c\u0000\u0000\u0a23"+
		"\u0a1e\u0001\u0000\u0000\u0000\u0a23\u0a21\u0001\u0000\u0000\u0000\u0a24"+
		"\u009f\u0001\u0000\u0000\u0000\u0a25\u0a26\u0005\u00c1\u0000\u0000\u0a26"+
		"\u0a2d\u0005\u00f5\u0000\u0000\u0a27\u0a28\u0005\u00c1\u0000\u0000\u0a28"+
		"\u0a2d\u00050\u0000\u0000\u0a29\u0a2a\u0005\u00c5\u0000\u0000\u0a2a\u0a2d"+
		"\u0005\u00c1\u0000\u0000\u0a2b\u0a2d\u0005\u00d9\u0000\u0000\u0a2c\u0a25"+
		"\u0001\u0000\u0000\u0000\u0a2c\u0a27\u0001\u0000\u0000\u0000\u0a2c\u0a29"+
		"\u0001\u0000\u0000\u0000\u0a2c\u0a2b\u0001\u0000\u0000\u0000\u0a2d\u00a1"+
		"\u0001\u0000\u0000\u0000\u0a2e\u0a34\u0003`0\u0000\u0a2f\u0a30\u0003\u00b6"+
		"[\u0000\u0a30\u0a31\u0005\u0015\u0000\u0000\u0a31\u0a32\u0003`0\u0000"+
		"\u0a32\u0a34\u0001\u0000\u0000\u0000\u0a33\u0a2e\u0001\u0000\u0000\u0000"+
		"\u0a33\u0a2f\u0001\u0000\u0000\u0000\u0a34\u00a3\u0001\u0000\u0000\u0000"+
		"\u0a35\u0a36\u0003\u00b6[\u0000\u0a36\u0a37\u0005\u0001\u0000\u0000\u0a37"+
		"\u0a38\u0003\u00b6[\u0000\u0a38\u0a3b\u0001\u0000\u0000\u0000\u0a39\u0a3b"+
		"\u0003\u00b6[\u0000\u0a3a\u0a35\u0001\u0000\u0000\u0000\u0a3a\u0a39\u0001"+
		"\u0000\u0000\u0000\u0a3b\u00a5\u0001\u0000\u0000\u0000\u0a3c\u0a41\u0003"+
		"\u00a4R\u0000\u0a3d\u0a3e\u0005\u0004\u0000\u0000\u0a3e\u0a40\u0003\u00a4"+
		"R\u0000\u0a3f\u0a3d\u0001\u0000\u0000\u0000\u0a40\u0a43\u0001\u0000\u0000"+
		"\u0000\u0a41\u0a3f\u0001\u0000\u0000\u0000\u0a41\u0a42\u0001\u0000\u0000"+
		"\u0000\u0a42\u00a7\u0001\u0000\u0000\u0000\u0a43\u0a41\u0001\u0000\u0000"+
		"\u0000\u0a44\u0a45\u0007\u001d\u0000\u0000\u0a45\u00a9\u0001\u0000\u0000"+
		"\u0000\u0a46\u0a4b\u0003\u00b6[\u0000\u0a47\u0a48\u0005\u0001\u0000\u0000"+
		"\u0a48\u0a4a\u0003\u00b6[\u0000\u0a49\u0a47\u0001\u0000\u0000\u0000\u0a4a"+
		"\u0a4d\u0001\u0000\u0000\u0000\u0a4b\u0a49\u0001\u0000\u0000\u0000\u0a4b"+
		"\u0a4c\u0001\u0000\u0000\u0000\u0a4c\u00ab\u0001\u0000\u0000\u0000\u0a4d"+
		"\u0a4b\u0001\u0000\u0000\u0000\u0a4e\u0a4f\u0005b\u0000\u0000\u0a4f\u0a50"+
		"\u0003\u00aeW\u0000\u0a50\u0a51\u0005\u001f\u0000\u0000\u0a51\u0a52\u0005"+
		"\u00a6\u0000\u0000\u0a52\u0a53\u0003h4\u0000\u0a53\u00ad\u0001\u0000\u0000"+
		"\u0000\u0a54\u0a55\u0007\u001e\u0000\u0000\u0a55\u00af\u0001\u0000\u0000"+
		"\u0000\u0a56\u0a5a\u0003\u00b2Y\u0000\u0a57\u0a5a\u0005>\u0000\u0000\u0a58"+
		"\u0a5a\u0005:\u0000\u0000\u0a59\u0a56\u0001\u0000\u0000\u0000\u0a59\u0a57"+
		"\u0001\u0000\u0000\u0000\u0a59\u0a58\u0001\u0000\u0000\u0000\u0a5a\u00b1"+
		"\u0001\u0000\u0000\u0000\u0a5b\u0a61\u0003\u00b6[\u0000\u0a5c\u0a5d\u0005"+
		"\u00fb\u0000\u0000\u0a5d\u0a61\u0003\u00b6[\u0000\u0a5e\u0a5f\u0005\u00cc"+
		"\u0000\u0000\u0a5f\u0a61\u0003\u00b6[\u0000\u0a60\u0a5b\u0001\u0000\u0000"+
		"\u0000\u0a60\u0a5c\u0001\u0000\u0000\u0000\u0a60\u0a5e\u0001\u0000\u0000"+
		"\u0000\u0a61\u00b3\u0001\u0000\u0000\u0000\u0a62\u0a67\u0003\u00b6[\u0000"+
		"\u0a63\u0a64\u0005\u0004\u0000\u0000\u0a64\u0a66\u0003\u00b6[\u0000\u0a65"+
		"\u0a63\u0001\u0000\u0000\u0000\u0a66\u0a69\u0001\u0000\u0000\u0000\u0a67"+
		"\u0a65\u0001\u0000\u0000\u0000\u0a67\u0a68\u0001\u0000\u0000\u0000\u0a68"+
		"\u00b5\u0001\u0000\u0000\u0000\u0a69\u0a67\u0001\u0000\u0000\u0000\u0a6a"+
		"\u0a70\u0005\u0120\u0000\u0000\u0a6b\u0a70\u0005\u0122\u0000\u0000\u0a6c"+
		"\u0a70\u0003\u00be_\u0000\u0a6d\u0a70\u0005\u0123\u0000\u0000\u0a6e\u0a70"+
		"\u0005\u0121\u0000\u0000\u0a6f\u0a6a\u0001\u0000\u0000\u0000\u0a6f\u0a6b"+
		"\u0001\u0000\u0000\u0000\u0a6f\u0a6c\u0001\u0000\u0000\u0000\u0a6f\u0a6d"+
		"\u0001\u0000\u0000\u0000\u0a6f\u0a6e\u0001\u0000\u0000\u0000\u0a70\u00b7"+
		"\u0001\u0000\u0000\u0000\u0a71\u0a73\u0005\u0113\u0000\u0000\u0a72\u0a71"+
		"\u0001\u0000\u0000\u0000\u0a72\u0a73\u0001\u0000\u0000\u0000\u0a73\u0a74"+
		"\u0001\u0000\u0000\u0000\u0a74\u0a7e\u0005\u011e\u0000\u0000\u0a75\u0a77"+
		"\u0005\u0113\u0000\u0000\u0a76\u0a75\u0001\u0000\u0000\u0000\u0a76\u0a77"+
		"\u0001\u0000\u0000\u0000\u0a77\u0a78\u0001\u0000\u0000\u0000\u0a78\u0a7e"+
		"\u0005\u011f\u0000\u0000\u0a79\u0a7b\u0005\u0113\u0000\u0000\u0a7a\u0a79"+
		"\u0001\u0000\u0000\u0000\u0a7a\u0a7b\u0001\u0000\u0000\u0000\u0a7b\u0a7c"+
		"\u0001\u0000\u0000\u0000\u0a7c\u0a7e\u0005\u011d\u0000\u0000\u0a7d\u0a72"+
		"\u0001\u0000\u0000\u0000\u0a7d\u0a76\u0001\u0000\u0000\u0000\u0a7d\u0a7a"+
		"\u0001\u0000\u0000\u0000\u0a7e\u00b9\u0001\u0000\u0000\u0000\u0a7f\u0a80"+
		"\u0005\u00aa\u0000\u0000\u0a80\u0a83\u0005\u0002\u0000\u0000\u0a81\u0a82"+
		"\u0005\u0120\u0000\u0000\u0a82\u0a84\u0005\u0001\u0000\u0000\u0a83\u0a81"+
		"\u0001\u0000\u0000\u0000\u0a83\u0a84\u0001\u0000\u0000\u0000\u0a84\u0a85"+
		"\u0001\u0000\u0000\u0000\u0a85\u0a86\u0005\u0119\u0000\u0000\u0a86\u0a87"+
		"\u0005\u0003\u0000\u0000\u0a87\u00bb\u0001\u0000\u0000\u0000\u0a88\u0a8b"+
		"\u0005+\u0000\u0000\u0a89\u0a8a\u0007\u001f\u0000\u0000\u0a8a\u0a8c\u0005"+
		"\u0001\u0000\u0000\u0a8b\u0a89\u0001\u0000\u0000\u0000\u0a8b\u0a8c\u0001"+
		"\u0000\u0000\u0000\u0a8c\u0a8d\u0001\u0000\u0000\u0000\u0a8d\u0a8e\u0007"+
		" \u0000\u0000\u0a8e\u00bd\u0001\u0000\u0000\u0000\u0a8f\u0a90\u0007!\u0000"+
		"\u0000\u0a90\u00bf\u0001\u0000\u0000\u0000\u0166\u00dc\u00e1\u00e5\u00eb"+
		"\u00ef\u0104\u0108\u010c\u0110\u0118\u011c\u011f\u0126\u012f\u0135\u0139"+
		"\u013f\u0146\u014f\u015b\u0164\u016a\u0175\u017d\u0185\u018c\u0196\u019d"+
		"\u01ba\u01bd\u01c0\u01c4\u01ca\u01cf\u01d6\u01db\u01df\u01e7\u01ed\u01f1"+
		"\u01ff\u0207\u021a\u0233\u0236\u0240\u0244\u024b\u0255\u025b\u0260\u0264"+
		"\u026a\u0273\u0279\u027d\u0284\u0288\u0290\u0295\u0299\u02a1\u02a9\u02ae"+
		"\u02b2\u02bc\u02c3\u02c8\u02cc\u02d6\u02d9\u02e2\u02e7\u02ed\u0305\u030b"+
		"\u030d\u0313\u0319\u031b\u0323\u0325\u032b\u0331\u0333\u0342\u0347\u034e"+
		"\u035a\u035c\u0364\u0366\u0378\u037b\u037f\u0383\u0395\u0398\u03a8\u03b2"+
		"\u03b7\u03bd\u03c0\u03c9\u03ce\u03d1\u03d4\u03d7\u03dc\u03e7\u03ea\u03f0"+
		"\u03f7\u03fc\u0402\u0406\u040a\u0410\u041b\u0424\u042e\u0431\u0436\u0438"+
		"\u043d\u0442\u0448\u044a\u044f\u0451\u0456\u0458\u045a\u045f\u0466\u0470"+
		"\u0476\u0479\u047b\u0487\u048e\u0492\u0496\u049a\u04a1\u04aa\u04ad\u04b1"+
		"\u04b6\u04ba\u04c2\u04c5\u04c8\u04cf\u04da\u04dd\u04e7\u04ea\u04f5\u04fa"+
		"\u0502\u0505\u0509\u0512\u051b\u051e\u0527\u052a\u052d\u0531\u053c\u053f"+
		"\u0546\u0549\u055c\u0560\u0564\u0568\u056c\u0570\u0572\u057d\u0582\u058b"+
		"\u0592\u0595\u059b\u05a7\u05aa\u05b3\u05b6\u05be\u05c1\u05c4\u05c9\u05cc"+
		"\u05d8\u05db\u05e3\u05e8\u05ec\u05ee\u05f0\u05ff\u0601\u060c\u0621\u062b"+
		"\u0636\u063a\u063c\u0644\u064b\u0658\u065e\u0662\u066b\u0671\u067e\u0685"+
		"\u0689\u0691\u0693\u069d\u06a1\u06a4\u06ab\u06bb\u06c3\u06cc\u06d2\u06da"+
		"\u06e0\u06e4\u06e9\u06ee\u06f7\u06ff\u0704\u0711\u071c\u071e\u072e\u0744"+
		"\u074f\u0757\u075c\u0761\u076e\u0774\u077b\u0780\u0783\u0786\u078b\u0792"+
		"\u0795\u079e\u07a1\u07a5\u07a8\u07ab\u07ba\u07bd\u07d0\u07d4\u07dc\u07e0"+
		"\u07f8\u0804\u0807\u0810\u0813\u081c\u0822\u0828\u082e\u0835\u083a\u0844"+
		"\u084d\u0863\u0866\u0869\u086f\u087a\u087c\u0885\u088b\u088e\u0896\u08a0"+
		"\u08a6\u08b4\u08bd\u08c4\u08c9\u08d0\u08da\u08df\u08e6\u0900\u0905\u0907"+
		"\u090e\u0912\u0919\u091d\u092e\u093d\u0944\u094d\u0957\u095c\u0965\u096a"+
		"\u0972\u097a\u097d\u0983\u0986\u098d\u0995\u0998\u09a0\u09a3\u09bd\u09c8"+
		"\u09cd\u09d4\u09d6\u09e3\u09f2\u09f6\u09fa\u09fe\u0a04\u0a08\u0a0c\u0a10"+
		"\u0a12\u0a1c\u0a23\u0a2c\u0a33\u0a3a\u0a41\u0a4b\u0a59\u0a60\u0a67\u0a6f"+
		"\u0a72\u0a76\u0a7a\u0a7d\u0a83\u0a8b";
	public static final String _serializedATN = Utils.join(
		new String[] {
			_serializedATNSegment0,
			_serializedATNSegment1
		},
		""
	);
	public static final ATN _ATN =
		new ATNDeserializer().deserialize(_serializedATN.toCharArray());
	static {
		_decisionToDFA = new DFA[_ATN.getNumberOfDecisions()];
		for (int i = 0; i < _ATN.getNumberOfDecisions(); i++) {
			_decisionToDFA[i] = new DFA(_ATN.getDecisionState(i), i);
		}
	}
}